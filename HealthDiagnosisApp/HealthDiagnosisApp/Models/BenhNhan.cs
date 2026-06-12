namespace HealthDiagnosisApp.Models
{
    public class BenhNhan
    {
        public List<string> DanhSachTrieuChung { get; set; } = new List<string>();
        public double ChieuCao { get; set; } // cm
        public double CanNang { get; set; } // kg
        public double BMI => CanNang / Math.Pow(ChieuCao / 100, 2);
    }

    public class DuLieuHuanLuyen
    {
        public BenhNhan DuLieuBenhNhan { get; set; }
        public string TenBenh { get; set; }
    }

    public class KetQuaKNN
    {
        public string BenhDuDoan { get; set; }
        public Dictionary<string, double> TyLeBenh { get; set; }
        public List<HangXom> HangXomGanNhat { get; set; }
        public string GiaiThichPhepTinh { get; set; }
        public int K { get; set; }
    }

    public class HangXom
    {
        public DuLieuHuanLuyen DuLieu { get; set; }
        public double KhoangCach { get; set; }
        public string TenBenh { get; set; }
    }
}
