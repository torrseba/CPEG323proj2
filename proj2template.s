.data
	prompt: .asciz "Enter a message (at most 22 characters):"
	prompt_size = .-prompt
	input_max_size = 24

.bss
	input: .space input_max_size

.text
.global _start
_start:
main:
	// Write sys call prints prompt message
	MOV x0, #1
	LDUR x1, =prompt
	LDUR x2, =prompt_size
	MOV x8, 0x40
	SVC 0

	// Read sys call to get the user input
	// save 2 extra bytes for the nonce we will add to the end of the message
	MOV x0, #1
	LDUR x1, =input
	MOV x2, #22
	MOV x8, 0x3f
	SVC 0

	// Mine for a coin
	// Trim size by 1 to remove new line character
	SUB x1, x0, #1
	LDUR x0, =input
	BL blue_hen_coin_mine

	exit:
	// Exit system call
	// This is so that a breakpoint can be set here to check what coins we have found after
	// we have finished coin mining
	MOV x8, #93
	SVC 0

/*
 * --- blue_hen_coin_value
 * Parameters
 *  x0 = blue hen hash
 * Returns
 *	x0 = coin value
 */
 blue_hen_coin_value:
 	BR LR

/*
 * --- blue_hen_coin_mine:
 * Parameters
 *  x0 = base address of string message
 *  x1 = size of string message in bytes
 * Returns
 *  x0 = nonce for most valuable coin
 *  x1 = value for most valuable coin
 *  x2 = total number of non-zero value coins in the entire search space
 */
blue_hen_coin_mine:
	BR LR
