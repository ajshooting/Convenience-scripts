<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Search Form</title>
</head>

<body>
    <h1>検索します。</h1>
    <h2>ごく一部の作品のみに対応しています。</h2>
    <form action="search.php" method="post">
        <label for="search_string">検索する文字列：</label>
        <input type="text" id="search_string" name="search_string">
        <input type="submit" value="検索">
    </form>

    <h5>対応作品</h5>
    <ul>
        <?php
        $counts = 0;
        $dirs = scandir('sub/');
        foreach ($dirs as $dir) {
            if (is_dir('sub/' . $dir) && $dir != '.' && $dir != '..') {
                $counts += 1;
                echo '<li>' . $dir . '</li>';
            }
        }
        echo "<br>合計" . $counts . "作品";
        ?>
    </ul>
    <h5>※中国語字幕混ざるかも</h5>
</body>

</html>