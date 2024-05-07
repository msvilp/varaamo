<script>
	import '@skeletonlabs/skeleton/themes/theme-skeleton.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
</script>

<style>
	/* Custom styles for the navbar */
	.list-nav {
		display: flex;
		flex-direction: column; /* Stack title and buttons vertically */
		align-items: center; /* Center items horizontally */
		padding: 1rem;
	}

	/* Ensure buttons are displayed below the title */
	.list-nav .title {
		margin-bottom: 1rem; /* Space between title and buttons */
	}
</style>

<!-- App Shell -->
<AppShell slotSidebarLeft="bg-surface-500/5 w-56 p-4">
	<svelte:fragment slot="sidebarLeft">
		<!-- App Bar -->
		<nav class="list-nav">
			<div class="title">
				<strong class="text-xl uppercase">Varaamo</strong>
			</div>
			<nav class="list-nav">
				<a href="/vuokraus/" target="_blank" rel="noreferrer">Vuokraus</a>
			</nav>
		</nav>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>
