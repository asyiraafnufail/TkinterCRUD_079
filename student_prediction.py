import mysql.connector #library mysql konektor
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk #library dari tkinter, pilih komponen yang diperlukan

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = mysql.connector.connect(host="localhost", user="root", password="") #variabel untuk koneksi ke database
    cursor = conn.cursor() #cursor.conn untuk mengarahkan koneksi ke database
    cursor.execute("CREATE DATABASE IF NOT EXISTS prediksi_siswa") #membuat database jika belum ada dengan nama "prediksi_siswa"
    cursor.execute("USE prediksi_siswa")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_siswa VARCHAR(255),
            biologi INT,
            fisika INT,
            inggris INT,
            prediksi_fakultas VARCHAR(255)
        ) 
    ''') #membuat table dan beserta tipe datanya
    conn.close() #mengakhiri koneksi ke database

#koneksi ke database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prediksi_siswa"
    )

#untuk mengambil data beserta menampilkannya
def fetch_data():
    conn = connect_to_db() #membuka koneksi ke database dengan bantuan fungsi connect_to_db
    cursor = conn.cursor() #cursor.conn untuk mengarahkan koneksi ke database
    cursor.execute("SELECT * FROM nilai_siswa") #mengambil data dari table nilai_siswa
    rows = cursor.fetchall() #mengambil semua data dari table dan diarahkan ke row
    conn.close() #mengakhiri koneksi ke database
    return rows

#untuk menambahkan data ke dalam database
def save_to_database(nama, biologi, fisika, inggris, prediksi): #fungsi untuk menyimpan data ke database beserta parameternya
    conn = connect_to_db() #membuka koneksi ke database dengan bantuan fungsi connect_to_db
    cursor = conn.cursor() #cursor.conn untuk mengarahkan koneksi ke database
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (%s, %s, %s, %s, %s) 
    ''', (nama, biologi, fisika, inggris, prediksi)) #query untuk menambahkan data ke dalam table nilai_siswa dengan nilai yang diisi dari parameter
    conn.commit() #mengirimkan perintah untuk menyimpan data ke database
    conn.close() #mengakhiri koneksi ke database
#fungsi untuk merubah/mengupdate data ke dalam database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = connect_to_db() #membuka koneksi ke database dengan bantuan fungsi connect_to_db
    cursor = conn.cursor() #cursor.conn untuk mengarahkan koneksi ke database
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = %s, biologi = %s, fisika = %s, inggris = %s, prediksi_fakultas = %s
        WHERE id = %s
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  #query untuk mengupdate data ke dalam table nilai_siswa dengan nilai yang diisi dari parameter
    conn.commit() #mengirimkan perintah untuk menyimpan data ke database
    conn.close() #mengakhiri koneksi ke database

#fungsi untuk menghapus data ke dalam database
def delete_database(record_id):
    conn = connect_to_db() #membuka koneksi ke database dengan bantuan fungsi connect_to_db
    cursor = conn.cursor() #cursor.conn untuk mengarahkan koneksi ke database
    cursor.execute('DELETE FROM nilai_siswa WHERE id = %s', (record_id,)) #query untuk menghapus data ke dalam table nilai_siswa dengan nilai yang diisi dari parameter
    conn.commit() #mengirimkan perintah untuk menyimpan data ke database
    conn.close() #mengakhiri koneksi ke database

#fungsi untuk syarat kondisi data
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

#fungsi tombol button untuk menyimpan data
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris) #membuat objek baru prediksi dan memanggil fungsi calculate prediction
        save_to_database(nama, biologi, fisika, inggris, prediksi) #memanggil fungsi untuk menyimpan data ke dalam database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}") #menampilkan message box untuk menginformasikan bahwa data telah disimpan atau tidak valid
        clear_inputs() #memanggil fungsi untuk mengosongkan inputan
        populate_table() #memanggil fungsi untuk menampilkan tabel hasil
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

#tombol button untuk update data
def update():
    try:
        if not selected_record_id.get(): #jika tidak ada syarat kondisi dimana id tidak boleh kosong
            raise Exception("Pilih data dari tabel untuk di-update!")

        #memanggil seluruh data dari database
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris) #membuat objek baru prediksi dan memanggil fungsi calculate prediction
        update_database(record_id, nama, biologi, fisika, inggris, prediksi) #memanggil fungsi untuk mengupdate data ke dalam database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!") #menampilkan message box untuk menginformasikan bahwa data telah diperbarui
        clear_inputs() #memanggil fungsi untuk mengosongkan inputan
        populate_table() #memanggil fungsi untuk menampilkan tabel hasil
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#tombol button fungsi menghapus data
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")
            record_id = int(selected_record_id.get()) #memanggil id yang ingin dihapus data dari database
        delete_database(record_id) #memanggil fungsi hapus data dari id yang dipilih
        messagebox.showinfo("Sukses", "Data berhasil dihapus!") #menampilkan message box untuk menginformasikan bahwa data telah dihapus
        clear_inputs() #memanggil fungsi untuk mengosongkan inputan
        populate_table() #memanggil fungsi untuk menampilkan tabel hasil
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#fungsi untuk mengosongkan inputan setelah mengisi inputan
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

#fungsi untuk menampilkan data berdasarkan tabel
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

#fungsi untuk event on click
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")
        
#main program dan tampilan

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar() #untuk menyimpan data nama
biologi_var = StringVar() # Untuk menyimpan nilai biologi record yang dipilih
fisika_var = StringVar() # Untuk menyimpan nilai fisika record yang dipilih
inggris_var = StringVar() # Untuk menyimpan nilai bahasa inggris record yang dipilih
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table) # Untuk mengisi inputan dengan data yang dipilih dari tabel yang ada dalam database ketiika setelah mengklik event
populate_table()

root.mainloop() # Untuk menjalankan aplikasi GUI