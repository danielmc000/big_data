import subprocess
import time
import webbrowser
from datetime import datetime
import os

# Colores (opcional para consola)
VERDE = "\033[92m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"

def ejecutar(script):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{AZUL}🕒 [{ahora}] Ejecutando: {script}{RESET}")
    try:
        resultado = subprocess.run(["python", script], capture_output=True, text=True)
        
        # Mostrar en consola
        print(VERDE + resultado.stdout + RESET)
        if resultado.stderr:
            print(ROJO + resultado.stderr + RESET)

        # Guardar en log.txt
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{ahora}] >>> {script}\n")
            f.write(resultado.stdout)
            if resultado.stderr:
                f.write(resultado.stderr)
            f.write("\n" + "="*60 + "\n")

    except Exception as e:
        error_msg = f"❌ Error al ejecutar {script}: {e}"
        print(ROJO + error_msg + RESET)
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{ahora}] >>> {script}\n")
            f.write(error_msg + "\n")
            f.write("\n" + "="*60 + "\n")

    print("-" * 60)

def lanzar_dashboard():
    print(AMARILLO + "🌐 Lanzando dashboard de Streamlit..." + RESET)
    subprocess.Popen(["streamlit", "run", "05_visualizacion.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

def flujo_constante(intervalo_minutos=5):
    dashboard_abierto = False
    while True:
        print(f"{AMARILLO}\n================ NUEVO CICLO DE FLUJO BIG DATA ================\n{RESET}")
        ejecutar("01_ingesta.py")
        ejecutar("02_almacenamiento.py")
        ejecutar("03_procesamiento_batch.py")
        ejecutar("04_procesamiento_streaming.py")

        if not dashboard_abierto:
            lanzar_dashboard()
            dashboard_abierto = True

        print(f"{AMARILLO}⏳ Esperando {intervalo_minutos} minutos para la próxima ejecución...{RESET}")
        time.sleep(intervalo_minutos * 60)

if __name__ == "__main__":
    flujo_constante(intervalo_minutos=5)
