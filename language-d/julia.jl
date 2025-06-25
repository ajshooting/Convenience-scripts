# Juliaもスクリプトとして実行可能

numbers = 1:10

# リスト内包表記で、一文で処理を記述。数学の集合の記法に似てる
sum_of_squares = sum(n^2 for n in numbers if n % 2 == 0)

println("Julia: The sum is ", sum_of_squares)