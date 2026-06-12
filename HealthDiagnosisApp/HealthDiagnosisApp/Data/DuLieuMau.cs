using HealthDiagnosisApp.Models;

namespace HealthDiagnosisApp.Data
{
    public static class DuLieuMau
    {
        public static List<DuLieuHuanLuyen> TaoDuLieuHuanLuyen()
        {
            return new List<DuLieuHuanLuyen>
        {
            // ==================== CẢM CÚM (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Ho", "Đau họng", "Sổ mũi", "Nhức đầu", "Mệt mỏi" },
                    ChieuCao = 170, CanNang = 65
                },
                TenBenh = "Cảm cúm"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Ho", "Sổ mũi", "Mệt mỏi" },
                    ChieuCao = 165, CanNang = 58
                },
                TenBenh = "Cảm cúm"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau họng", "Sổ mũi", "Nhức đầu", "Mệt mỏi" },
                    ChieuCao = 175, CanNang = 70
                },
                TenBenh = "Cảm cúm"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Ho", "Nhức đầu" },
                    ChieuCao = 160, CanNang = 55
                },
                TenBenh = "Cảm cúm"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Đau họng", "Mệt mỏi" },
                    ChieuCao = 180, CanNang = 75
                },
                TenBenh = "Cảm cúm"
            },

            // ==================== VIÊM HỌNG (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau họng", "Sốt", "Khó nuốt", "Ho khan" },
                    ChieuCao = 168, CanNang = 62
                },
                TenBenh = "Viêm họng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau họng dữ dội", "Sốt cao", "Nhức đầu" },
                    ChieuCao = 172, CanNang = 68
                },
                TenBenh = "Viêm họng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau họng", "Khàn giọng", "Ho" },
                    ChieuCao = 158, CanNang = 52
                },
                TenBenh = "Viêm họng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Đau họng", "Sưng hạch" },
                    ChieuCao = 185, CanNang = 80
                },
                TenBenh = "Viêm họng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau họng", "Nhức đầu", "Mệt mỏi" },
                    ChieuCao = 162, CanNang = 57
                },
                TenBenh = "Viêm họng"
            },

            // ==================== VIÊM PHỔI (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt cao", "Ho có đờm", "Khó thở", "Đau ngực" },
                    ChieuCao = 175, CanNang = 72
                },
                TenBenh = "Viêm phổi"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Khó thở", "Sốt", "Mệt mỏi nặng", "Đau ngực khi thở" },
                    ChieuCao = 169, CanNang = 64
                },
                TenBenh = "Viêm phổi"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Ho liên tục", "Sốt", "Ớn lạnh", "Khó thở" },
                    ChieuCao = 182, CanNang = 78
                },
                TenBenh = "Viêm phổi"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau ngực", "Ho có đờm vàng", "Sốt" },
                    ChieuCao = 166, CanNang = 60
                },
                TenBenh = "Viêm phổi"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Khó thở khi vận động", "Ho", "Mệt mỏi" },
                    ChieuCao = 178, CanNang = 74
                },
                TenBenh = "Viêm phổi"
            },

            // ==================== COVID-19 (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Ho khan", "Mất vị giác", "Mất khứu giác" },
                    ChieuCao = 171, CanNang = 66
                },
                TenBenh = "COVID-19"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Khó thở", "Đau cơ", "Mệt mỏi" },
                    ChieuCao = 164, CanNang = 59
                },
                TenBenh = "COVID-19"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Ho", "Sốt nhẹ", "Mất vị giác", "Đau họng" },
                    ChieuCao = 176, CanNang = 71
                },
                TenBenh = "COVID-19"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Mệt mỏi", "Đau đầu", "Mất khứu giác", "Sổ mũi" },
                    ChieuCao = 163, CanNang = 58
                },
                TenBenh = "COVID-19"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Ho", "Khó thở nhẹ", "Đau cơ" },
                    ChieuCao = 179, CanNang = 76
                },
                TenBenh = "COVID-19"
            },

            // ==================== DẠ DÀY (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau bụng", "Buồn nôn", "Ợ chua", "Chán ăn" },
                    ChieuCao = 167, CanNang = 63
                },
                TenBenh = "Dạ dày"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau thượng vị", "Buồn nôn", "Ợ nóng" },
                    ChieuCao = 173, CanNang = 69
                },
                TenBenh = "Dạ dày"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau bụng sau ăn", "Buồn nôn", "Đầy bụng" },
                    ChieuCao = 159, CanNang = 54
                },
                TenBenh = "Dạ dày"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Ợ chua", "Đau bụng", "Khó tiêu" },
                    ChieuCao = 181, CanNang = 77
                },
                TenBenh = "Dạ dày"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Buồn nôn", "Đau bụng", "Chán ăn" },
                    ChieuCao = 161, CanNang = 56
                },
                TenBenh = "Dạ dày"
            },

            // ==================== DỊ ỨNG (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Phát ban", "Ngứa", "Sổ mũi", "Hắt hơi" },
                    ChieuCao = 174, CanNang = 67
                },
                TenBenh = "Dị ứng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Ngứa mắt", "Hắt hơi", "Sổ mũi" },
                    ChieuCao = 168, CanNang = 61
                },
                TenBenh = "Dị ứng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Phát ban", "Khó thở", "Sưng mặt" },
                    ChieuCao = 177, CanNang = 73
                },
                TenBenh = "Dị ứng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Hắt hơi liên tục", "Ngứa mũi", "Chảy nước mắt" },
                    ChieuCao = 155, CanNang = 50
                },
                TenBenh = "Dị ứng"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Phát ban", "Ngứa", "Sổ mũi" },
                    ChieuCao = 170, CanNang = 65
                },
                TenBenh = "Dị ứng"
            },

            // ==================== SỐT XUẤT HUYẾT (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt cao đột ngột", "Đau đầu dữ dội", "Xuất huyết", "Đau cơ" },
                    ChieuCao = 172, CanNang = 68
                },
                TenBenh = "Sốt xuất huyết"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Xuất huyết dưới da", "Buồn nôn" },
                    ChieuCao = 166, CanNang = 60
                },
                TenBenh = "Sốt xuất huyết"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt cao", "Đau sau hốc mắt", "Đau cơ khớp" },
                    ChieuCao = 180, CanNang = 75
                },
                TenBenh = "Sốt xuất huyết"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt", "Xuất huyết", "Mệt mỏi" },
                    ChieuCao = 164, CanNang = 59
                },
                TenBenh = "Sốt xuất huyết"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Sốt cao", "Đau đầu", "Buồn nôn", "Xuất huyết nhẹ" },
                    ChieuCao = 178, CanNang = 74
                },
                TenBenh = "Sốt xuất huyết"
            },

            // ==================== VIÊM GAN (10 mẫu) ====================
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Mệt mỏi", "Vàng da", "Vàng mắt", "Đau hạ sườn phải" },
                    ChieuCao = 175, CanNang = 70
                },
                TenBenh = "Viêm gan"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Chán ăn", "Buồn nôn", "Mệt mỏi", "Vàng da" },
                    ChieuCao = 169, CanNang = 64
                },
                TenBenh = "Viêm gan"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Đau bụng", "Sốt nhẹ", "Vàng mắt" },
                    ChieuCao = 182, CanNang = 78
                },
                TenBenh = "Viêm gan"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Mệt mỏi kéo dài", "Chán ăn", "Đau hạ sườn" },
                    ChieuCao = 167, CanNang = 62
                },
                TenBenh = "Viêm gan"
            },
            new DuLieuHuanLuyen {
                DuLieuBenhNhan = new BenhNhan {
                    DanhSachTrieuChung = new List<string> { "Vàng da", "Buồn nôn", "Ngứa" },
                    ChieuCao = 173, CanNang = 69
                },
                TenBenh = "Viêm gan"
            }
        };
        }
    }
}
