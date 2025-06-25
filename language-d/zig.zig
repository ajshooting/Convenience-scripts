// Zig

const std = @import("std");
const print = std.debug.print;

pub fn main() void {
    const numbers = [_]i32{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    var sum: i32 = 0;
    
    for (numbers) |n| {
        if (n % 2 == 0) {
            sum += n * n;
        }
    }
    
    print("Zig: The sum is {}\n", .{sum});
}
