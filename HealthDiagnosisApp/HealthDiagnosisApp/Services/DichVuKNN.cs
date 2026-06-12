using HealthDiagnosisApp.Data;
using HealthDiagnosisApp.Models;
using System.Text;

namespace HealthDiagnosisApp.Services
{
    public class DichVuKNN
    {
        private List<DuLieuHuanLuyen> _duLieuHuanLuyen;

        public DichVuKNN()
        {
            _duLieuHuanLuyen = DuLieuMau.TaoDuLieuHuanLuyen();
        }

        public KetQuaKNN DuDoanBenh(BenhNhan benhNhan, int k)
        {
            // 1. Tính khoảng cách Euclid đến từng điểm dữ liệu
            var hangXomVoiKhoangCach = new List<HangXom>();

            foreach (var duLieu in _duLieuHuanLuyen)
            {
                double khoangCach = TinhKhoangCachEuclid(benhNhan, duLieu.DuLieuBenhNhan);
                hangXomVoiKhoangCach.Add(new HangXom
                {
                    DuLieu = duLieu,
                    KhoangCach = khoangCach,
                    TenBenh = duLieu.TenBenh
                });
            }

            // 2. Sắp xếp theo khoảng cách và lấy K hàng xóm gần nhất
            var hangXomGanNhat = hangXomVoiKhoangCach
                .OrderBy(h => h.KhoangCach)
                .Take(k)
                .ToList();

            // 3. Đếm phiếu cho từng bệnh
            var demBenh = hangXomGanNhat
                .GroupBy(h => h.TenBenh)
                .ToDictionary(g => g.Key, g => g.Count());

            // 4. Xử lý trường hợp hòa phiếu
            string benhDuDoan;
            var giaiThich = new StringBuilder();

            if (demBenh.Values.Distinct().Count() == 1) // Tất cả bằng nhau
            {
                // Chọn bệnh có khoảng cách trung bình nhỏ nhất
                benhDuDoan = demBenh.Keys
                    .OrderBy(ben => hangXomGanNhat
                        .Where(h => h.TenBenh == ben)
                        .Average(h => h.KhoangCach))
                    .First();

                giaiThich.AppendLine("Các bệnh có số phiếu bằng nhau. ");
                giaiThich.AppendLine($"Chọn {benhDuDoan} vì có khoảng cách trung bình nhỏ nhất.");
            }
            else
            {
                benhDuDoan = demBenh.OrderByDescending(x => x.Value).First().Key;
                giaiThich.AppendLine($"{benhDuDoan} có số phiếu cao nhất ({demBenh[benhDuDoan]}/{k}).");
            }

            // 5. Tính tỷ lệ phần trăm
            var tyLeBenh = demBenh.ToDictionary(
                x => x.Key,
                x => Math.Round((double)x.Value / k * 100, 2)
            );

            // 6. Tạo giải thích chi tiết
            giaiThich.AppendLine($"\nChi tiết {k} hàng xóm gần nhất:");
            foreach (var hangXom in hangXomGanNhat)
            {
                giaiThich.AppendLine($"- {hangXom.TenBenh}: Khoảng cách = {Math.Round(hangXom.KhoangCach, 2)}");
            }

            return new KetQuaKNN
            {
                BenhDuDoan = benhDuDoan,
                TyLeBenh = tyLeBenh,
                HangXomGanNhat = hangXomGanNhat,
                GiaiThichPhepTinh = giaiThich.ToString(),
                K = k
            };
        }

        private double TinhKhoangCachEuclid(BenhNhan bn1, BenhNhan bn2)
        {
            // Chuyển triệu chứng thành vector nhị phân
            var tatCaTrieuChung = TrieuChung.DanhSachTrieuChung;
            double tongBinhPhuong = 0;

            // Khoảng cách cho triệu chứng (nhị phân)
            foreach (var trieuChung in tatCaTrieuChung)
            {
                int coTrieuChung1 = bn1.DanhSachTrieuChung.Contains(trieuChung) ? 1 : 0;
                int coTrieuChung2 = bn2.DanhSachTrieuChung.Contains(trieuChung) ? 1 : 0;
                tongBinhPhuong += Math.Pow(coTrieuChung1 - coTrieuChung2, 2);
            }

            // Khoảng cách cho BMI (chuẩn hóa)
            double bmi1 = bn1.BMI;
            double bmi2 = bn2.BMI;
            double bmiChuanHoa = (bmi1 - bmi2) / 10; // Giả sử độ lệch chuẩn BMI là 10

            tongBinhPhuong += Math.Pow(bmiChuanHoa, 2);

            return Math.Sqrt(tongBinhPhuong);
        }
    }
}
