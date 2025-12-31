<script context="module" lang="ts">
    import type { RangeKey } from "$lib/utils/range";

    export type RangeTreeNode = {
        label: string;
        rangeKey?: RangeKey;
        children?: RangeTreeNode[];
    }
</script>

<script lang="ts">
    import RangeTree from './RangeTree.svelte'
    import { selectedRange } from '$lib/stores/rangeStore'
    import { PokerRange } from '$lib/utils/range'

    export let nodes: RangeTreeNode[] = []

    // Track which nodes are expanded
    let expandedNodes: Set<RangeTreeNode> = new Set()

    async function select(node: RangeTreeNode) {
        console.log(node.rangeKey)
        if (!node.rangeKey) {
            if (expandedNodes.has(node)) {
                expandedNodes.delete(node)
            } else {
                expandedNodes.add(node)
            }
            expandedNodes = new Set(expandedNodes)
            return
        }

        selectedRange.set(null)
        const range = await PokerRange.create(node.rangeKey)
        selectedRange.set(range)
    }
</script>

<ul>
    {#each nodes as node}
        <li>
            <button class="node" on:click={() => select(node)}>
                {#if expandedNodes.has(node) && !node.rangeKey}
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                    </svg>
                {:else if !expandedNodes.has(node) && !node.rangeKey}
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width={1.5} stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                    </svg>
                {/if}
                
                <p>{node.label}</p>
            </button>

            {#if node.children && expandedNodes.has(node)}
                <RangeTree nodes={node.children} />
            {/if}
        </li>
    {/each}
</ul>

<style>
    ul {
        margin: 0;
        list-style: none;
        padding-left: 2.5rem;
    }

    svg {
        width: 1rem;
        height: 1rem;
    }

    .node {
        display: flex;
        align-items: center;
        padding: 0.0rem 1.0rem;
        color: var(--fg);
        background: none;
        border: none;
        width: 100%;
    }

    .node > p {
        margin-left: 1rem;
    }

    .node:hover {
        background: var(--bg-muted);
    }
</style>
