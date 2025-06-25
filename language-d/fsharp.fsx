// F#

let numbers = [1..10]
let sumOfSquares =
    numbers
    |> List.filter (fun n -> n % 2 = 0)
    |> List.map (fun n -> n * n)
    |> List.sum

printfn "F#: The sum is %d" sumOfSquares
