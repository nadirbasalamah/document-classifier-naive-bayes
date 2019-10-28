<?php
//inisialisasi variabel
$total = 0;
$res = array();
$sample = array();
$bag_of_words = array();
$term_freq = array();
$doc_freq = array();
$hasil_filter = array();
$documents = array();
$terms = array();
$file_stopwords = file_get_contents("stopwords.txt"); //membaca file yang berisi daftar stop word
$stopwords = preg_split('/[\s-]+/',$file_stopwords); //mengubah isi file menjadi array
//fungsi untuk menghilangkan stop word
function removeStopword($word,$stopwords_list)
{   
    $result = false;
    //melakukan pencarian kata yang terdapat pada daftar stop word
    for ($i=0; $i < count($stopwords_list); $i++) { 
        if (strcmp(strtolower($word),$stopwords_list[$i]) === 0) {
            $result = true;
            break;
        }
    }
    return $result;
}
//fungsi untuk melakukan preprocessing
function preprocessing($document,$stopwords_list)
{
    $result = array();
    for ($i=0; $i < count($document); $i++) { 
        if (removeStopword($document[$i],$stopwords_list) !== true && $document[$i] !== "") {
            array_push($result,strtolower($document[$i]));
        }
    }
    return $result;
}
//fungsi untuk mendapatkan sekumpulan kata (term)
function getBagOfWords($words)
{
    $result = array();
    for ($i=0; $i < count($words); $i++) { 
        for ($j=0; $j < count($words[$i]); $j++) { 
            array_push($result,$words[$i][$j]);
        }
    }
    return $result;
}
//fungsi untuk menghitung tf pada setiap dokumen
function getTermFrequency($words)
{
    $tf = array_count_values($words);
    return $tf;
}
//fungsi untuk mendapatkan tf pada kata tertentu
function getSingleTf($tf,$word,$total)
{
    $res = array();
    $itr = 0;
    for ($i=0; $i < count($tf); $i++) { 
        foreach ($tf[$i] as $key => $value) {
            if ($word === $key) {
                array_push($res,$value);
            }
        }
    }

    if (count($res) !== $total) {
        $itr = $total - count($res);
        for ($i=0; $i < $itr; $i++) { 
            array_push($res,0);
        }
    }

    return $res;
}
//fungsi untuk menghitung tf-idf pada setiap kata
function calculateTfIdf($tf,$df,$total)
{
    $res = 0;
    if ($tf === 0 || $df === 0) {
        return $res;
    } else {
        $res = round((1 + log10($tf)) * log10($total / $df),3);
    }
    return $res;
}

//fungsi untuk menghitung df
function getDocumentFrequency($tf,$word)
{
    $df = 0;
    for ($i=0; $i < count($tf); $i++) { 
        foreach ($tf[$i] as $key => $value) {
            if ($word === $key) {
                $df++;
            }
        }
    }
    return $df;
}
//fungsi untuk menghitung pembobotan tf-idf
function getTfIdf($tf,$df,$total)
{
    $termfreq = array();
    $result = array();
    for ($i=0; $i < count($tf); $i++) { 
        foreach ($tf[$i] as $key => $value) {
            array_push($termfreq,$value);
        }
    }
    for ($i=0; $i < count($df); $i++) { 
        for ($j=0; $j < count($termfreq); $j++) { 
            $result[$i] = round((1 + log10($termfreq[$j])) * log10($total / $df[$i]),3);
        }
    }
    return $result;
}

//melakukan proses upload dan perhitungan tf-idf ketika tombol Unggah File diklik
if (isset($_POST['upload'])) {
    $total = count($_FILES['dokumen']['name']);
    for ($i=0; $i < $total; $i++) { 
        $target_path = "uploads/"; 
        $target_path = $target_path . basename($_FILES['dokumen']['name'][$i]); 
        $fileParts = pathinfo($target_path); //mengambil info file
        //jika file berekstensi txt dan ditemukan maka dilakukan perhitungan tf-idf
        if(move_uploaded_file($_FILES['dokumen']['tmp_name'][$i], $target_path) && $fileParts['extension'] == "txt") {        
            $isi_file = file_get_contents($target_path); //mengambil isi file
            //memecah isi file menjadi array dan menghilangkan tanda baca pada dokumen teks
            $dokumen = preg_split('/[\s,.–()-?!]+/',$isi_file); 
            $documents[$i] = $dokumen;
            $hasil_filter[$i] = preprocessing($documents[$i],$stopwords);  //melakukan preprocessing
            $terms[$i] = array_values(array_unique($hasil_filter[$i]));
            echo "File ".  basename( $_FILES['dokumen']['name'][$i]). " berhasil diunggah";
          } else {
            echo "Unggah file gagal, format file tidak cocok";
          }
    }
    $bag_of_words = getBagOfWords($terms);
    for ($i=0; $i < $total; $i++) { 
        $term_freq[$i] = getTermFrequency($hasil_filter[$i]);
    }
    for ($i=0; $i < count($terms); $i++) { 
        for ($j=0; $j < count($terms[$i]); $j++) { 
            array_push($doc_freq,getDocumentFrequency($term_freq,$terms[$i][$j]));
        }
    }
    for ($i=0; $i < count($terms); $i++) { 
        for ($j=0; $j < count($terms[$i]); $j++) { 
            array_push($sample,getSingleTf($term_freq,$terms[$i][$j],$total));
        }
    }
    
    $res = getTfIdf($term_freq,$doc_freq,$total);
}
?>
<!--bagian Front-End-->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Simple Text Document Preprocessing</title>
    <style>
    table, th, td {
    border: 1px solid black;
    }
    </style>
</head>
<body>
    <h1>Simple Text Document Indexing</h1>
    <h3>Sebuah program untuk melakukan pembobotan dalam sebuah dokumen teks</h3>
    <p>Referensi stopwords yang digunakan : <a href="http://hikaruyuuki.lecture.ub.ac.id/kamus-kata-dasar-dan-stopword-list-bahasa-indonesia/" target="_blank">Link</a></p>
    <p>Unggah file dokumen teks dalam format txt</p>
    <!--form digunakan untuk mengunggah file dokumen teks dalam bentuk file txt-->
    <form action="#" method="post" enctype="multipart/form-data">
        <input type="file" name="dokumen[]" id="dokumen" multiple="multiple">
        <input type="submit" value="Unggah file" name="upload">
    </form>
    <!--menampilkan hasil pembobotan dengan tf-idf-->
    <h2>Hasil Pembobotan</h2>
    <?php
        if (empty($hasil_filter) == true) {
            echo "";
        } else {
            $ratio = (count($hasil_filter) / count($dokumen)) * 100;
            echo "Rasio dari hasil preprocessing : " . round($ratio,2) . "%";
        }
    ?>
    <table style="width:25%">
    <tr>
        <th>Nomor</th>
        <th>Indeks (term)</th> 
        <?php
        $counter = 1;
        if ($total != 0) {
            for ($i=0; $i < $total; $i++) { 
                echo "<th> Dokumen "  . $counter++ . "</th>";
            }
        }
        ?>
    </tr>
    <?php 
    $count = 1;
    if (empty($bag_of_words) !== true) {
        for ($i=0; $i < count($bag_of_words); $i++) {
            echo "<tr>";
            echo "<td>" . $count++ . "</td>";
            echo "<td>" . $bag_of_words[$i] . "</td>";
            for ($j=0; $j < count($sample[$i]); $j++) { 
                echo "<td>" . calculateTfIdf($sample[$i][$j],$doc_freq[$i],$total) . "</td>";
            }
            echo "</tr>";  
        }
    } else {
        echo "";
    }
    ?>
    <table style="width:10%">
    <tr>
        <th>Nomor</th>
        <th>Df</th>
    </tr>
    <?php 
    $count = 1;
    if (empty($doc_freq) !== true) {
        foreach ($doc_freq as $key => $value) {
            echo "<tr>";
            echo "<td>" . $count++ . "</td>";
            echo "<td>" . $value . "</td>";
            echo "</tr>";
        } 
    } else {
        echo "";
    }
    ?>
    </table>
</body>
</html>