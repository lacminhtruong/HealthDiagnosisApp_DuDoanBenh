using HealthDiagnosisApp.Models;
using HealthDiagnosisApp.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthDiagnosisApp.Controllers
{
    public class ChanDoanController : Controller
    {
        private readonly DichVuKNN _dichVuKNN;

        public ChanDoanController()
        {
            _dichVuKNN = new DichVuKNN();
        }

        public IActionResult Index()
        {
            var benhNhan = new BenhNhan
            {
                DanhSachTrieuChung = new List<string>() // khởi tạo list rỗng để tránh null
            };

            ViewBag.DanhSachTrieuChung = TrieuChung.DanhSachTrieuChung;
            return View(benhNhan); // ✅ truyền model xuống view
        }


        [HttpPost]
        public IActionResult KetQua(BenhNhan benhNhan, int k = 5)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.DanhSachTrieuChung = TrieuChung.DanhSachTrieuChung;
                return View("Index", benhNhan);
            }

            var ketQua = _dichVuKNN.DuDoanBenh(benhNhan, k);
            return View(ketQua);
        }
    }
}
