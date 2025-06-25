# Nim

let numbers = @[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
let sumOfSquares = numbers.filterIt(it mod 2 == 0).mapIt(it * it).sum()

echo "Nim: The sum is ", sumOfSquares
