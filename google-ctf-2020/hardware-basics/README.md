# Basics

> With all those CPU bugs I don't trust software anymore, so I came up with my custom TPM (trademark will be filed soon!). You can't break this, so don't even try.
> 
> basics.2020.ctfcompetition.com 1337

This challenge gives us two files:

- `check.sv`, a SystemVerilog file that describes a `check` module with an `open_safe` output;
- `main.cpp`, which asks for a password, feeds it to the `check` module and prints the flag if `open_safe` is true.

We need to understand the conditions that will set `open_safe` to true, so let's take a closer look at `check.sv`.

```verilog
module check(
    input clk,

    input [6:0] data,
    output wire open_safe
);
```

The `[6:0]` notation represents a 7 bit wide bus, with the least significant bit on the right (index 0) and the most significant bit on the left (index 6). The module receives 7 bits of input at a time, which corresponds to an ASCII character.

```verilog
reg [6:0] memory [7:0];
reg [2:0] idx = 0;
```

There are 8 `memory` registers, each one 7 bits wide, and a single `idx` register, 3 bits wide and initially set to 0.

```verilog
wire [55:0] magic = {
    {memory[0], memory[5]},
    {memory[6], memory[2]},
    {memory[4], memory[3]},
    {memory[7], memory[1]}
};

wire [55:0] kittens = { magic[9:0],  magic[41:22], magic[21:10], magic[55:42] };
assign open_safe = kittens == 56'd3008192072309708;
```

Now comes some wire tangling. The `magic` wire reoders the `memory` registers and the `kittens` wire reorders the `magic` wire. `open_safe` will be true if the output of `kittens` is equal to the decimal number 3008192072309708, so we'll need to untangle this. We can already infer that our password is 8 characters wide, for a total of 7 × 8 = 56 bits.

```verilog
always_ff @(posedge clk) begin
    memory[idx] <= data;
    idx <= idx + 5;
end
```

At each clock cycle, the input data is saved to the `idx` index of `memory`. Notice, however, that `idx` is 3 bits wide and we're adding 5 a few times, so `idx` will overflow and its value will wrap around.

Let's use `abcdefgh` as our input to see how this module will behave at each clock cycle:

1. `idx` = 0; `memory[0] <= 'a'`; `idx <= idx + 5`;
2. `idx` = 5; `memory[5] <= 'b'`; `idx <= idx + 5`; (Overflow!)
3. `idx` = 2; `memory[2] <= 'c'`; `idx <= idx + 5`;
4. `idx` = 7; `memory[7] <= 'd'`; `idx <= idx + 5`; (Overflow!)
5. `idx` = 4; `memory[4] <= 'e'`; `idx <= idx + 5`; (Overflow!)
6. `idx` = 1; `memory[1] <= 'f'`; `idx <= idx + 5`;
7. `idx` = 6; `memory[6] <= 'g'`; `idx <= idx + 5`; (Overflow!)
8. `idx` = 3; `memory[3] <= 'h'`; `idx <= idx + 5`;

Therefore, from `memory[0]` to `memory[7]` we have `{a, f, c, h, e, b, g, d}`. The `magic` wire reorders those registers once again, which results in `{a, b, g, c, e, h, d, f}`.

We need `kittens` to be equal to 3008192072309708, which is 00001010101011111110111101001011111000101101101111001100 in binary (notice the left zeroes to have exactly 56 bits). The first 10 bits of `kittens` correspond to `magic[9:0]`, the next 20 bits correspond to `magic[41:22]` and so on. By rearranging those bits, we can find out what value we need `magic` to have:

```
kittens = { magic[9:0],  magic[41:22],          magic[21:10],  magic[55:42]   }
            0000101010 | 10111111101111010010 | 111110001011 | 01101111001100

          { magic[55:42],    magic[41:22],          magic[21:10],  magic[9:0] }
            01101111001100 | 10111111101111010010 | 111110001011 | 0000101010
```

Now we know the value of `magic` should be 01101111001100101111111011110100101111100010110000101010. If we split this value into groups of 7 bits, we'll find the following ASCII characters: `7L_o%xX*`. We also know that if our input is `abcdefgh` the value of `magic` will be `{a, b, g, c, e, h, d, f}`, so if we want `magic` to be `7L_o%xX*` we can reverse the logic:

```
abgcehdf => abcdefgh
7L_o%xX* => 7LoX%*_x
```

By submitting `7LoX%*_x` as the password, we obtain our flag!

Flag: `CTF{W4sTh4tASan1tyCh3ck?}`
