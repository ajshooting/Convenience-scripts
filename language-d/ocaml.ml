(* OCaml *)

let () =
  let numbers = [1;2;3;4;5;6;7;8;9;10] in
  let sum_of_squares =
    numbers
    |> List.filter (fun n -> n mod 2 = 0)
    |> List.map (fun n -> n * n)
    |> List.fold_left (+) 0
  in
  Printf.printf "OCaml: The sum is %d\n" sum_of_squares
