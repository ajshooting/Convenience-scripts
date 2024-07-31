<?php
// search.php

function search_string_in_files($folder_path, $search_string)
{
    $count = 0;
    $folder_count = 0;
    $file_count = 0;
    $lines_count = 0;
    $files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($folder_path));
    foreach ($files as $file) {
        if ($file->isFile()) {
            $file_path = $file->getRealPath();
            try {
                $lines = file($file_path);
                foreach ($lines as $i => $line) {
                    $lines_count++;
                    if (strpos($line, $search_string) !== false) {
                        $count++;
                        echo "<span style='color:black'>[$folder_count] [" . str_replace('', '', $file_path) . "]</span><br>";
                        if (trim($lines[$i - 3]) !== "" && $i > 2) {
                            echo "　： <span style='color:black'>" . trim($lines[$i - 3]) . "</span><br>";
                        }
                        if (trim($lines[$i - 2]) !== "" && $i > 1) {
                            echo "　： <span style='color:black'>" . trim($lines[$i - 2]) . "</span><br>";
                        }
                        if (trim($lines[$i - 1]) !== "" && $i > 0) {
                            echo "　： <span style='color:black'>" . trim($lines[$i - 1]) . "</span><br>";
                        }
                        echo "○： <span style='color:red'>" . trim($line) . "</span><br>";
                        echo "　： <span style='color:black'>" . trim($lines[$i + 1]) . "</span><br>";
                        echo "<br>";
                    }
                }
            } catch (Exception $e) {
                echo "ファイル \"" . basename($file_path) . "\" の読み込み中にエラーが発生しました：$e<br>";
            }
        } else if ($file->isDir()) {
            $folder_count++;
        }
    }
    echo "<span style='color:black'>";
    echo "合計: ${count}件 / ${lines_count}行<br>";
}

if (isset($_POST['search_string'])) {
    echo "<a href='search_form.php'>戻る</a>";
    echo "<br>検索文字列[" . $_POST['search_string'] . "]<br><br>";
    $folder_path = "sub";
    $search_string = $_POST['search_string'];
    $start_time = microtime(true);
    search_string_in_files($folder_path, $search_string);
    $end_time = microtime(true);
    $execution_time = ($end_time - $start_time);
    echo "処理時間: " . $execution_time . " 秒";



    echo "</span>";

} else {
    header('Location: search_form.php');
}