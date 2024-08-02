<script lang=ts>
    import { displayWidth } from "../stores";
	export let leftInitialSize = '50%';

	let left: HTMLElement;
	let isDragging = false;

	function dragstart() {
		isDragging = true;
	}

	function drag(e: MouseEvent) {
		if (!isDragging) return;

		const elementLeft = left.getBoundingClientRect().left;
		left.style.flexBasis = e.clientX - elementLeft + 'px';
	}

	function dragend() {
		if (!isDragging) return;

		isDragging = false;
	}
    $: console.log($displayWidth)
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="split-pane" on:mousemove={drag} on:mouseup={dragend} bind:clientWidth={$displayWidth}>
	<div bind:this={left} class="left" style="flex-basis: {leftInitialSize}">
		<slot name="left" />
	</div>
	<div class="splitter" on:mousedown={dragstart} />
	<div class="right">
		<slot name="right" />
	</div>
</div>

<style>
	.splitter {
		flex-grow: 0;
		flex-shrink: 0;
		width: 5px;
		background-color: rgb(65, 65, 65);
		cursor: col-resize;
	}

	.split-pane {
		display: flex;
		align-items: stretch;
		width: 100%;
        max-height: 80vh;
	}

	.split-pane > div {
		display: block;
	}

	.left {
		flex-grow: 0;
		flex-shrink: 0;
	}

	.right {
		flex-grow: 1;
		flex-shrink: 1;
		overflow-x: auto;
	}
</style>