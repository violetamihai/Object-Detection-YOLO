import tkinter as tk  # Importam modulul tkinter si il redenumim ca tk
import subprocess  # Importam modulul subprocess pentru a putea rula alte programe

class VideoApp:  # Definim clasa VideoApp
    def __init__(self, root):  # Definim constructorul pentru clasa VideoApp, cu argumentul root
        self.root = root  # Setam variabila self.root cu valoarea argumentului root

        # Configuram fereastra principala
        self.root.title("Comanda camera de supraveghere")  # Setam titlul ferestrei 
        self.root.geometry("400x250")  # Setam dimensiunea ferestrei la 400x250 pixeli

        # Cream un buton pentru a porni fluxul video
        self.live_button = tk.Button(self.root, text="Vezi camera live", command=self.start_stream,
                                      font=("Arial", 12), bd=2, relief="raised", bg="#4CAF50", fg="white")
        self.live_button.pack(pady=5)  # Plasam butonul in fereastra

        # Cream un buton pentru a porni supravegherea fara a afisa fluxul video
        self.start_button = tk.Button(self.root, text="Incepe supravegherea", command=self.start_surveillance,
                                       font=("Arial", 12), bd=2, relief="raised", bg="#FFC107", fg="black")
        self.start_button.pack(pady=5)  # Plasam butonul in fereastra

        # Cream un buton pentru a opri fluxul video
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_stream,  # Command-ul butonului este stop_stream
                                      state=tk.DISABLED, font=("Arial", 12), bd=2, relief="raised", bg="#F44336", fg="white")
        self.stop_button.pack(pady=5)  # Plasam butonul in fereastra

        # Legam evenimentul de inchidere a ferestrei de functia close_window
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)  

    def start_stream(self):  # Definim functia pentru a porni fluxul video
        try:  # Incercam sa rulam procesul
            self.process = subprocess.Popen(["python", "C:/Users/Violeta/Desktop/AMp/main.py"],  # Pornim programul principal
                                              startupinfo=subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW))
            self.live_button.config(state=tk.DISABLED)  # Dezactivam butonul Vezi camera live
            self.start_button.config(state=tk.DISABLED)  # Dezactivam butonul Incepe supravegherea
            self.stop_button.config(state=tk.NORMAL)  # Activam butonul Stop Stream
        except Exception as e:  # In caz de eroare
            print("Error:", e)  # Afisam eroarea

    def start_surveillance(self):  # Definim functia pentru a porni supravegherea fara afisarea fluxului video
        try:  # Incercam sa rulam procesul
            self.process = subprocess.Popen(["python", "C:/Users/Violeta/Desktop/AMp/supraveghere.py"],  # Pornim programul de supraveghere
                                              startupinfo=subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW))
            self.live_button.config(state=tk.DISABLED)  # Dezactivam butonul Vezi camera live
            self.start_button.config(state=tk.DISABLED)  # Dezactivam butonul Incepe supravegherea
            self.stop_button.config(state=tk.NORMAL)  # Activam butonul Stop Stream
        except Exception as e:  # In caz de eroare
            print("Error:", e)  # Afisam eroarea

    def stop_stream(self):  # Definim functia pentru a opri fluxul video
        if hasattr(self, 'process') and self.process.poll() is None:  # Daca procesul este inca activ
            self.process.terminate()  # Terminam procesul
            self.live_button.config(state=tk.NORMAL)  # Activam butonul Vezi camera live
            self.start_button.config(state=tk.NORMAL)  # Activam butonul Incepe supravegherea
            self.stop_button.config(state=tk.DISABLED)  # Dezactivam butonul Stop Stream

    def close_window(self):  # Definim functia pentru a inchide fereastra
        self.stop_stream()  # Apelam functia pentru a opri fluxul video
        self.root.destroy()  # Distruge fereastra

def main():  # Definim functia principala
    root = tk.Tk()  # Initializam o fereastra tkinter
    app = VideoApp(root)  # Cream o instanta a clasei VideoApp
    root.mainloop()  # Rulam bucla evenimentelor

if __name__ == "__main__":  # Daca acest script este rulat direct
    main()  # Apelam functia main
