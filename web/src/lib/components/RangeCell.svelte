<script lang="ts">
    import type { HandAction, Range, Rank } from '$lib/utils/range';
    import { RANKS } from '$lib/utils/range';

    export let row: Rank;
    export let col: Rank;
    export let range: Range;

    function getHandLabel(row: Rank, col: Rank): string {
        const i = RANKS.indexOf(row);
        const j = RANKS.indexOf(col);

        if (i === j) return row + col;
        if (i < j) return row + col + 's';
        return col + row + 'o';
    }

    function getActionColor(actionName: string): string {
        switch (actionName) {
            case 'call': return 'var(--call)';
            case 'raise': return 'var(--raise)';
            case 'allin': return 'var(--allin)';
            default: return '#ffffff';
        }
    }

    const hand = getHandLabel(row, col);
    const actions: HandAction[] = range.get(hand) ?? [];
    const totalFreq = actions.reduce((acc, a) => acc + a.freq, 0);
</script>

<div class="cell" title="{hand}">
    <div class="cell-labels {totalFreq === 0 ? 'inactive' : ''}">
        <span class="hand">{hand}</span>
    </div>
    {#each actions as handAction, i}
        <div
        class="bar"
        style="
            width: {handAction.freq * 100}%;
            background-color: {getActionColor(handAction.action.name)};
            left: {actions.slice(0, i).reduce((sum, a) => sum + a.freq, 0) * 100}%;
        "
        ></div>
    {/each}
</div>

<style>
    .cell {
        position: relative;
        width: 100%;
        height: 100%;
        font-family: 'Fira Code', monospace;
        display: flex;
        flex-direction: column;
        justify-content: flex-begin;
        border: 1px solid var(--border);
        background-color: var(--bg-muted);
        overflow: hidden;
        cursor: default;
        padding: 5px;
        box-sizing: border-box;
    }

    .bar {
        position: absolute;
        bottom: 0;
        height: 100%;
        z-index: 0;
    }

    .cell-labels {
        color: var(--fg);
        font-size: 16px;
        z-index: 1;
    }

    .inactive {
        color: #797593;
    }
</style>
