// Scala

val numbers = 1 to 10
val sumOfSquares = numbers
  .filter(_ % 2 == 0)
  .map(n => n * n)
  .sum

println(s"Scala: The sum is $sumOfSquares")
