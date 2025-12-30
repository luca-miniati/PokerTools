import { writable } from 'svelte/store'
import type { Range } from '$lib/utils/range'

export const selectedRange = writable<Range | null>(null)
