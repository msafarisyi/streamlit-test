import streamlit as st
import threading
import subprocess
import os
import sys
import time
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Pastikan folder hasil simulasi tersedia
SIMULATION_FOLDER = "simulation_results"
os.makedirs(SIMULATION_FOLDER, exist_ok=True)

class PathSelector:
    def __init__(self):
        st.title("Simulator PyQt")

        # **Inisialisasi session state jika belum ada**
        if "num_sim" not in st.session_state:
            st.session_state.num_sim = 1

        if "sim_status" not in st.session_state:
            st.session_state.sim_status = {}

        if "sim_images" not in st.session_state:
            st.session_state.sim_images = {}

        # **Deteksi perubahan jumlah simulasi**
        def update_num_sim():
            st.session_state.num_sim = st.session_state.num_sim_input

        st.number_input(
            "Jumlah simulasi",
            min_value=1,
            max_value=10,
            value=st.session_state.num_sim,
            key="num_sim_input",
            help="Pilih jumlah simulasi.",
            on_change=update_num_sim
        )

        # **Tombol Refresh untuk memperbarui status & gambar**
        if st.button("Refresh Status & Gambar"):
            st.rerun()

        # **Loop untuk membuat form simulasi**
        for i in range(st.session_state.num_sim):
            with st.container():
                st.header(f"Simulasi {i+1}")

                video_name = st.text_input(label="VIDEO NAME", key=f"video_name_{i+1}")
                random_text = st.text_input(label="RANDOM TEXT", key=f"random_text_{i+1}")

                # **Inisialisasi status simulasi jika belum ada**
                if f"sim_status_{i+1}" not in st.session_state:
                    st.session_state[f"sim_status_{i+1}"] = "Waiting..."

                # **Tempat untuk status dan gambar hasil simulasi**
                status_placeholder = st.empty()
                image_placeholder = st.empty()

                # **Update status simulasi**
                status_placeholder.markdown(f"**Status:** {st.session_state[f'sim_status_{i+1}']}")

                # **Tombol untuk menjalankan simulasi**
                if st.button(label=f"START SIMULATION {i+1}", key=f"submit_button_{i+1}"):
                    # **Hapus gambar sebelumnya sebelum simulasi baru dimulai**
                    st.session_state.pop(f"sim_image_{i+1}", None)

                    st.session_state[f"sim_status_{i+1}"] = "Simulation in Process..."
                    status_placeholder.markdown(f"**Status:** {st.session_state[f'sim_status_{i+1}']}")

                    # **Jalankan simulasi dalam thread**
                    thread_simulation = threading.Thread(
                        target=self.run_simulation,
                        args=(i+1,)
                    )
                    add_script_run_ctx(thread_simulation)
                    thread_simulation.start()

                # **Tampilkan gambar hasil simulasi di dalam container terkait**
                if f"sim_image_{i+1}" in st.session_state:
                    image_path = st.session_state[f"sim_image_{i+1}"]
                    if image_path and os.path.exists(image_path):
                        image_placeholder.image(image_path, caption=f"Simulation {i+1} Result", use_container_width=True)

    def run_simulation(self, simulation_id):
        """Menjalankan simulasi di subprocess"""
        image_path = self.execSimulation(simulation_id)

        # **Simpan path gambar ke session state**
        if image_path:
            st.session_state[f"sim_image_{simulation_id}"] = image_path

        # **Perbarui status setelah simulasi selesai**
        st.session_state[f"sim_status_{simulation_id}"] = "Simulation End"

    def execSimulation(self, simulation_id):
        """Eksekusi subprocess untuk menjalankan simulasi"""
        python_executable = sys.executable
        command = [python_executable, "-u", "simulation.py", str(simulation_id)]

        print(f"Executing: {' '.join(command)}")

        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            process.wait()  # Tunggu proses selesai

            # **Ambil gambar hasil simulasi**
            time.sleep(1)  # Beri waktu agar file tersimpan
            files = sorted(
                [f for f in os.listdir(SIMULATION_FOLDER) if f.endswith(".png")],
                key=lambda x: os.path.getmtime(os.path.join(SIMULATION_FOLDER, x)),
                reverse=True
            )

            if files:
                image_path = os.path.join(SIMULATION_FOLDER, files[0])
                print(f"Simulation {simulation_id} End! Image saved at {image_path}")
                return image_path
            else:
                print(f"Simulation {simulation_id} End! No image found.")
                return None

        except Exception as e:
            print(f"Exception: {e}")
            return None

if __name__ == '__main__':
    PathSelector()
