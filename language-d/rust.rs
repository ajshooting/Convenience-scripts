fn main() {
    // Rustでは `Vec<i32>` のように型を厳密に定義
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // `into_iter()`でデータを消費するイテレータに変換し、処理を繋げてく
    let sum_of_squares: i32 = numbers
        .into_iter()
        .filter(|n| n % 2 == 0) // 偶数だけをフィルタリング
        .map(|n| n * n)         // 残った要素をそれぞれ2乗
        .sum();                 // 最後に合計する

    println!("Rust: The sum is {}", sum_of_squares);
}