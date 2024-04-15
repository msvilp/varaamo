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

	/* Add space between buttons */
	.list-nav .btn-spaced {
		margin-bottom: 0.5rem; /* Adjust the value as needed */
	}
</style>

<!-- App Shell -->
<AppShell slotSidebarLeft="bg-surface-500/5 w-56 p-4">
	<svelte:fragment slot="sidebarLeft">
		<!-- App Bar -->
		<nav class="list-nav">
			<div class="title">
				<strong class="text-xl uppercase">Skeleton</strong>
			</div>
			<nav class="list-nav">
				<a class="btn btn-sm btn-ghost-surface btn-spaced" href="https://discord.gg/EXqV7W8MtY" target="_blank" rel="noreferrer">Discord</a>
				<a class="btn btn-sm btn-ghost-surface btn-spaced" href="https://twitter.com/SkeletonUI" target="_blank" rel="noreferrer">Twitter</a>
				<a class="btn btn-sm btn-ghost-surface btn-spaced" href="https://github.com/skeletonlabs/skeleton" target="_blank" rel="noreferrer">GitHub</a>
				<a href="/" target="_blank" rel="noreferrer">Vuokraus</a>
			</nav>
		</nav>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>
