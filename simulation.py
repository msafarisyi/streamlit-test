import sys
import os
import time
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Pastikan folder hasil simulasi tersedia
SIMULATION_FOLDER = "simulation_results"
os.makedirs(SIMULATION_FOLDER, exist_ok=True)

class Simulation:
    def __init__(self, width=400, height=300):
        """Inisialisasi simulasi dengan ukuran gambar tertentu."""
        self.width = width
        self.height = height

    def run(self, sim_id):
        """Menjalankan simulasi dan menyimpan hasil gambar."""
        logging.info(f"Simulation {sim_id} Starting...")

        # Inisialisasi aplikasi PyQt (harus dibuat di dalam metode ini)
        app = QApplication([])

        try:
            # Buat gambar
            pixmap = QPixmap(self.width, self.height)
            pixmap.fill(Qt.white)

            # Gambar dengan QPainter
            painter = QPainter(pixmap)
            pen = QPen(Qt.black)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(50, 50, self.width - 50, self.height - 50)
            painter.drawText(60, 80, f"Hasil Simulasi {sim_id}")
            painter.end()

            # Simpan gambar ke file
            image_filename = f"sim_{sim_id}_{int(time.time())}.png"
            image_path = os.path.join(SIMULATION_FOLDER, image_filename)
            
            if pixmap.save(image_path):
                logging.info(f"Gambar berhasil disimpan: {image_path}")
            else:
                logging.error(f"Gagal menyimpan gambar ke: {image_path}")

            logging.info(f"Simulation {sim_id} End.")

        except Exception as e:
            logging.exception(f"Terjadi kesalahan dalam simulasi {sim_id}: {e}")

        finally:
            app.exit()

# Jalankan simulasi jika dijalankan langsung
if __name__ == "__main__":
    if len(sys.argv) > 1:
        sim_id = sys.argv[1]
    else:
        sim_id = "default"

    sim = Simulation()
    sim.run(sim_id)
