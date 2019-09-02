require 'securerandom'
require 'openssl'

ROUNDS = 765
BITS = 128
PAIRS = 6

def encrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = (enc + key) & mask
        enc = enc ^ key
    end
    enc
end

def decrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = enc ^ key
        enc = (enc - key) & mask
    end
    enc
end

plain = [
	0x029abc13947b5373b86a1dc1d423807a,
	0xeeb83b72d3336a80a853bf9c61d6f254,
	0x7a0e5ffc7208f978b81475201fbeb3a0,
	0xc464714f5cdce458f32608f8b5e2002e,
	0xf944aaccf6779a65e8ba74795da3c41d,
	0x552682756304d662fa18e624b09b2ac5
]

enc = [
	"b36b6b62a7e685bd1158744662c5d04a",
	"614d86b5b6653cdc8f33368c41e99254",
	"292a7ff7f12b4e21db00e593246be5a0",
	"64f930da37d494c634fa22a609342ffe",
	"aa3825e62d053fb0eb8e7e2621dabfe7",
	"f2ffdf4beb933681844c70190ecf60bf"
]

# We know nothing about the key yet, so for now it's an empty string
known_key = ""
# We'll start comparing two characters
size = 2
# We'll save our encryption results here
new_enc = []
# Compare results go here
compare = []

# Repeat for each character of the key, except the last one
for char in 1..31
	# Guess one byte at a time
	for guess in 0x0..0xff
		# Add our guess to what we already have
		key = (guess.to_s(16) + known_key).to_i(16)

		# Encrypt with the key and compare the results
		for i in 0..5
			new_enc[i] = encrypt(plain[i], key).to_s(16)
			len1 = new_enc[i].length
			len2 = enc[i].length
			compare[i] = (new_enc[i][len1 - size, len1] == enc[i][len2 - size, len2])
		end

		# If they're all equal, we have a candidate
		if compare[0] && compare[1] && compare[2] && compare[3] && compare[4] && compare[5] then
			# Show the key so far
			puts key.to_s(16)
			# Get the new candidate
			new_char = key.to_s(16)[1]
		end
	end
	# Increase comparison size
	size = size + 1
	# Append the new character to what we already have
	known_key = new_char + known_key
end
