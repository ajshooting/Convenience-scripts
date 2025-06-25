# Crystal

numbers = [1,2,3,4,5,6,7,8,9,10]
sum_of_squares = numbers.select(&.even?).map { |n| n * n }.sum
puts "Crystal: The sum is #{sum_of_squares}"
