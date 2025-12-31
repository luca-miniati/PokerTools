import { writable } from 'svelte/store'
import type { PokerRange } from '$lib/utils/range'

export const selectedRange = writable<PokerRange | null>(null)
