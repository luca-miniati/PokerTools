<script lang="ts">
    import { selectedRange } from '$lib/stores/rangeStore';

    function getActionType(action: string): string {
        return action.split(' ')[0].toLowerCase();
    }
</script>

{#if $selectedRange}
    <p>{$selectedRange.getName()}</p>
    <div class="actions-container">
        {#each Object.entries($selectedRange.getAggregateStrategy()) as [action, freq]}
            <div class="action-row">
                <div
                    class="action-box"
                    style="background-color: var(--{getActionType(action)});"
                ></div>
                {action}: {(freq * 100).toFixed(2)}%
            </div>
        {/each}
    </div>
{:else}
    Select a range
{/if}

<style>
    p {
        margin: 0;
    }

    .actions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 3.0rem;
        align-items: center;
    }

    .action-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.25rem;
    }

    .action-box {
        width: 16px;
        height: 16px;
        margin-right: 0.5rem;
        flex-shrink: 0;
    }
</style>