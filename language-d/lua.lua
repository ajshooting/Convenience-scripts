-- `local`で変数のスコープを限定するのが良い習慣
local numbers = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }
local sum_of_squares = 0

-- `ipairs`でテーブル（配列）を順番に処理
for _, n in ipairs(numbers) do
    if n % 2 == 0 then
        -- 条件に合うものを、合計用の変数に足す
        sum_of_squares = sum_of_squares + (n * n)
    end
end

-- `..` は文字列の連結演算子
print("Lua: The sum is " .. sum_of_squares)
