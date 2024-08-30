---
title: QRIS Information
---

Sebelum anda melakukan transaksi menggunakan QRIS pada endpoint <span style="color:#C75151">**POST**</span> **`/api/v1/transaction/qris`**,
mungkin anda butuh untuk menterjemahkan code QRIS menjadi informasi untuk ditampilkan pada aplikasi anda. Untuk itu saya
menyediakan sebuah endpoint khusus dan terlepas dari versioning `/api/v1/`.

---

## EndPoint for Get Information

<span style="color:#C75151">**GET**</span> **`/qris`**

- **Summary:** Non authentication request for parse QRIS content to data json

???+ "Content Example"

    === "Response"
            
        ``` { .json .copy }
        {
            "message": "ok",
            "status": true,
            "data": {
                "raw": "00020101021126550016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE51440014ID.CO.QRIS.WWW0215ID20190022915550303UBE5204839853033605802ID5906Baznas6013Jakarta Pusat61051034062070703A016304A402",
                "format_indicator": "01",
                "initiation_method": "11",
                "amount": "",
                "merchant_name": "Baznas",
                "merchant_city": "Jakarta Pusat",
                "country_code": "ID",
                "postal_code": "10340",
                "merchant_account_1": {
                    "identifier": "ID.CO.SHOPEE.WWW",
                    "merchant_id": "18",
                    "merchant_pan": "936009180000000018",
                    "merchant_criteria": "UBE"
                },
                "merchant_account_2": {
                    "identifier": "ID.CO.QRIS.WWW",
                    "merchant_id": "ID2019002291555",
                    "merchant_pan": "",
                    "merchant_criteria": "UBE"
                },
                "additional_info": {
                    "reference_label": "",
                    "terminal_label": "A01",
                    "payment_system_specified_template": ""
                },
                "crc": "A402"
            }
        }
        ```

    === "Request"

        ``` { .shell .copy }
        curl --location --request GET 'https://ppob-fake-api.fly.dev/qris?content=00020101021126550016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE51440014ID.CO.QRIS.WWW0215ID20190022915550303UBE5204839853033605802ID5906Baznas6013Jakarta Pusat61051034062070703A016304A402' \
        ```

---

## Struktur QRIS untuk Parsing dan Penjelasannya

QRIS (Quick Response Code Indonesian Standard) adalah standar kode QR yang digunakan di Indonesia untuk memfasilitasi
pembayaran digital. Struktur QRIS mengikuti format EMVCo yang mencakup berbagai elemen data yang diparsing dari kode QR.
Berikut adalah struktur umum QRIS dan penjelasan dari masing-masing elemennya:

### 1. **Payload Format Indicator (ID 00)**

- **Format**: Dua digit
- **Deskripsi**: Indikator versi format, umumnya bernilai "01" untuk QRIS.

### 2. **Point of Initiation Method (ID 01)**

- **Format**: Dua digit
- **Deskripsi**: Metode inisiasi, bernilai "11" jika QR statis (untuk transaksi banyak kali) atau "12" jika QR dinamis (
  untuk transaksi sekali).

### 3. **Merchant Account Information (ID 26-51)**

- **Format**: Struktur data yang terdiri dari sub-elemen
- **Deskripsi**: Informasi terkait akun merchant, dapat mencakup beberapa sub-elemen, seperti:
    - **ID 00**: Globally Unique Identifier (GUID) untuk merchant.
    - **ID 01**: Nomor ID merchant.
    - **ID 02**: PAN (Primary Account Number) merchant.
    - **ID 03**: Kriteria spesifik merchant.

### 4. **Merchant Category Code (ID 52)**

- **Format**: Empat digit
- **Deskripsi**: Kode yang menunjukkan kategori bisnis merchant (e.g., 5311 untuk supermarket).

### 5. **Transaction Currency (ID 53)**

- **Format**: Tiga digit
- **Deskripsi**: Kode mata uang transaksi, umumnya "360" untuk IDR (Rupiah Indonesia).

### 6. **Transaction Amount (ID 54)**

- **Format**: Nilai angka
- **Deskripsi**: Jumlah nominal transaksi, bisa kosong jika menggunakan QR statis.

### 7. **Tip or Convenience Fee Indicator (ID 55)**

- **Format**: Dua digit
- **Deskripsi**: Indikator tip atau biaya layanan.

### 8. **Country Code (ID 58)**

- **Format**: Dua karakter
- **Deskripsi**: Kode negara, umumnya "ID" untuk Indonesia.

### 9. **Merchant Name (ID 59)**

- **Format**: String (alfanumerik)
- **Deskripsi**: Nama merchant.

### 10. **Merchant City (ID 60)**

- **Format**: String (alfanumerik)
- **Deskripsi**: Kota tempat merchant berada.

### 11. **Postal Code (ID 61)**

- **Format**: String (alfanumerik)
- **Deskripsi**: Kode pos lokasi merchant.

### 12. **Additional Data Field Template (ID 62)**

- **Format**: Struktur data yang terdiri dari sub-elemen
- **Deskripsi**: Informasi tambahan yang mungkin diperlukan, seperti:
    - **ID 01**: Label referensi.
    - **ID 05**: Label terminal.
    - **ID 07**: Label pengguna.

### 13. **CRC (ID 63)**

- **Format**: Empat digit heksadesimal
- **Deskripsi**: Cyclic Redundancy Check (CRC) untuk validasi integritas data.

### Penjelasan Tambahan:

1. **Penggunaan ID dan Sub-ID**: Struktur QRIS menggunakan ID untuk menandai berbagai elemen data, dan beberapa elemen
   seperti Merchant Account Information dan Additional Data Field Template dapat memiliki sub-ID.

2. **Panjang Data**: Setiap ID diikuti oleh dua digit yang menunjukkan panjang data dalam karakter, diikuti oleh data
   aktual. Contohnya, `010211` berarti ID 01 (Point of Initiation Method) memiliki panjang data 02 karakter dengan
   nilai "11".

3. **Parsing**: Untuk memparsing QRIS, prosesnya melibatkan pembacaan ID, mengekstrak panjang data, dan kemudian
   mengambil data yang sesuai. Data kemudian dapat diproses lebih lanjut atau ditampilkan sesuai kebutuhan.


## Langkah-langkah Parsing

### Pseudo Code Explanation

```shell
function qris_processor(result: dict) -> QrisData:
    initialize qris_data as new QrisData object

    define mapping as dictionary with:
        "00" -> "format_indicator"
        "01" -> "initiation_method"
        "54" -> "amount"
        "59" -> "merchant_name"
        "60" -> "merchant_city"
        "58" -> "country_code"
        "61" -> "postal_code"
        "26-00" -> "merchant_account_1.identifier"
        "26-01" -> "merchant_account_1.merchant_pan"
        "26-02" -> "merchant_account_1.merchant_id"
        "26-03" -> "merchant_account_1.merchant_criteria"
        "51-00" -> "merchant_account_2.identifier"
        "51-01" -> "merchant_account_2.merchant_pan"
        "51-02" -> "merchant_account_2.merchant_id"
        "51-03" -> "merchant_account_2.merchant_criteria"
        "62-05" -> "additional_info.reference_label"
        "62-07" -> "additional_info.terminal_label"
        "62-50" -> "additional_info.payment_system_specified_template"
        "63" -> "crc"

    for each key-value pair (t, u) in result:
        if t exists in mapping:
            split the mapped attribute path into list attr_path
            set target as qris_data

            for each attribute in attr_path except the last one:
                update target to point to the corresponding attribute of target

            set the last attribute of target to value u

    return qris_data


function parse_qris(input_string: str) -> Optional[QrisData]:
    initialize index as 0
    initialize result as an empty dictionary

    while index is less than length of input_string:
        extract qr_id as substring from index to index + 2
        extract qr_id_length as substring from index + 2 to index + 4

        try to convert qr_id_length to integer qr_id_value_length:
            if conversion fails, return None

        extract qr_id_value as substring from index + 4 to index + 4 + qr_id_value_length
        store qr_id_value in result with key qr_id

        if qr_id is between 26 and 40 or in [51, 62]:
            initialize nested_index as 0

            while nested_index is less than length of qr_id_value:
                try to extract nested qr_id as substring from nested_index to nested_index + 2
                extract nqi_length as substring from nested_index + 2 to nested_index + 4
                convert nqi_length to integer nqi_value_length

                calculate nqi_value_index as nested_index + 4
                calculate nqi_value_index_offset as nested_index + 4 + nqi_value_length

                extract nqi_value as substring from nqi_value_index to nqi_value_index_offset
                store nqi_value in result with key "qr_id-nqi"

                update nested_index by adding 4 + nqi_value_length
                if any extraction or conversion fails, return None

        update index by adding 4 + qr_id_value_length

    call qris_processor with result and store the returned object in qris_data
    set raw attribute of qris_data to input_string

    if qris_data.merchant_account_2.identifier equals 'ID.CO.QRIS.WWW':
        return qris_data
    else:
        return None  # invalid QRIS provider

```

### Contoh QRIS:

![qris.png](images/qris.png)

Berikut adalah penjelasan step by step untuk memproses QRIS berdasarkan
contoh input berikut:

```
00020101021126550016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE51440014ID.CO.QRIS.WWW0215ID20190022915550303UBE5204839853033605802ID5906Baznas6013Jakarta Pusat61051034062070703A016304A402
```

### 1. Memulai `parse_qris`:

- **Index** dimulai dari `0`.
- **Result** adalah dictionary kosong.

### 2. Memproses QRIS secara bertahap:

#### Iterasi 1:

- **qr_id**: `00` (dari index `0-2`)
- **qr_id_length**: `02` (dari index `2-4`)
- **qr_id_value_length**: `2`
- **qr_id_value**: `01` (dari index `4-6`)
- **Result**: `{"00": "01"}`

- **Index** sekarang menjadi `6`.

#### Iterasi 2:

- **qr_id**: `01`
- **qr_id_length**: `02`
- **qr_id_value_length**: `2`
- **qr_id_value**: `11`
- **Result**: `{"00": "01", "01": "11"}`

- **Index** sekarang menjadi `10`.

#### Iterasi 3:

- **qr_id**: `26` (Merupakan Merchant Account)
- **qr_id_length**: `55`
- **qr_id_value_length**: `55`
- **qr_id_value**: `0016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE`
- **Result**: `{"00": "01", "01": "11", "26": "0016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE"}`

- **Index** sekarang menjadi `69`.

**Nested Iterasi dalam `26`:**

- **nqi**: `00`
- **nqi_length**: `16`
- **nqi_value**: `ID.CO.SHOPEE.WWW`
- **Result**:
  `{"00": "01", "01": "11", "26": "0016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE", "26-00": "ID.CO.SHOPEE.WWW"}`

- **nqi**: `01`
- **nqi_length**: `18`
- **nqi_value**: `936009180000000018`
- **Result**: `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018"}`

- **nqi**: `02`
- **nqi_length**: `02`
- **nqi_value**: `18`
- **Result**: `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18"}`

- **nqi**: `03`
- **nqi_length**: `03`
- **nqi_value**: `UBE`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE"}`

#### Iterasi 4:

- **qr_id**: `51` (Merupakan Merchant Account 2)
- **qr_id_length**: `44`
- **qr_id_value_length**: `44`
- **qr_id_value**: `0014ID.CO.QRIS.WWW0215ID20190022915550303UBE`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51": "0014ID.CO.QRIS.WWW0215ID20190022915550303UBE"}`

- **Index** sekarang menjadi `117`.

**Nested Iterasi dalam `51`:**

- **nqi**: `00`
- **nqi_length**: `14`
- **nqi_value**: `ID.CO.QRIS.WWW`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW"}`

- **nqi**: `02`
- **nqi_length**: `15`
- **nqi_value**: `ID2019002291555`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555"}`

- **nqi**: `03`
- **nqi_length**: `03`
- **nqi_value**: `UBE`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE"}`

#### Iterasi 5:

- **qr_id**: `52`
- **qr_id_length**: `04`
- **qr_id_value_length**: `4`
- **qr_id_value**: `8398`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398"}`

- **Index** sekarang menjadi `127`.

#### Iterasi 6:

- **qr_id**: `53`
- **qr_id_length**: `03`
- **qr_id_value_length**: `3`
- **qr_id_value**: `360`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360"}`

- **Index** sekarang menjadi `134`.

#### Iterasi 7:

- **qr_id**: `58`
- **qr_id_length**: `02`
- **qr_id_value_length**: `2`
- **qr_id_value**: `ID`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360", "58": "ID"}`

- **Index** sekarang menjadi `138`.

#### Iterasi 8:

- **qr_id**: `59`
- **qr_id_length**: `06`
- **qr_id_value_length**: `6`
- **qr_id_value**: `Baznas`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360", "58": "ID", "59": "Baznas"}`

- **Index** sekarang menjadi `148`.

#### Iterasi 9:
-

**qr_id**: `60`

- **qr_id_length**: `13`
- **qr_id_value_length**: `13`
- **qr_id_value**: `Jakarta Pusat`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360", "58": "ID", "59": "Baznas", "60": "Jakarta Pusat"}`

- **Index** sekarang menjadi `165`.

#### Iterasi 10:

- **qr_id**: `61`
- **qr_id_length**: `05`
- **qr_id_value_length**: `5`
- **qr_id_value**: `10340`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360", "58": "ID", "59": "Baznas", "60": "Jakarta Pusat", "61": "10340"}`

- **Index** sekarang menjadi `174`.

#### Iterasi 11:

- **qr_id**: `62` (Additional Info)
- **qr_id_length**: `07`
- **qr_id_value_length**: `7`
- **qr_id_value**: `03A0163`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360", "58": "ID", "59": "Baznas", "60": "Jakarta Pusat", "61": "10340", "62": "03A0163"}`

- **Index** sekarang menjadi `183`.

#### Iterasi 12:

- **qr_id**: `63`
- **qr_id_length**: `04`
- **qr_id_value_length**: `4`
- **qr_id_value**: `A402`
- **Result**:
  `{"00": "01", "01": "11", "26-00": "ID.CO.SHOPEE.WWW", "26-01": "936009180000000018", "26-02": "18", "26-03": "UBE", "51-00": "ID.CO.QRIS.WWW", "51-02": "ID2019002291555", "51-03": "UBE", "52": "8398", "53": "360", "58": "ID", "59": "Baznas", "60": "Jakarta Pusat", "61": "10340", "62-07": "03A0163", "63": "A402"}`

- **Index** sekarang menjadi `191`, yang merupakan akhir dari string input.

### 3. Memanggil `qris_processor`

- Setelah semua data diparsing, `qris_processor` akan memetakan data dari `Result` ke atribut `QrisData`.
- **Raw** dari `qris_data` diisi dengan `input_string`.

### 4. Memvalidasi QRIS:

- Memeriksa apakah `merchant_account_2.identifier` sama dengan `'ID.CO.QRIS.WWW'`.
- Jika ya, kembalikan `qris_data`.
- Jika tidak, kembalikan `None`.

### 5. Hasil Akhir

- Berdasarkan contoh di atas, data QRIS valid, dan `qris_data` yang diproses akan dikembalikan, berisi informasi lengkap
  seperti `merchant_name` (`Baznas`), `merchant_city` (`Jakarta Pusat`), `amount`, dan lainnya sesuai dengan hasil
  parsing.

---

## Core reference

[utsmannn/qris_parser.py](https://gist.github.com/utsmannn/06ef96e12237ff622de687d5b582630f)