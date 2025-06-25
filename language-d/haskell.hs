-- Haskell

main :: IO ()
main = do
  let numbers = [1..10]
      sumOfSquares = sum $ map (^2) $ filter even numbers
  putStrLn $ "Haskell: The sum is " ++ show sumOfSquares
