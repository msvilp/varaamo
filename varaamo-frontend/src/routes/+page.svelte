<script lang="ts">
	import type { PageData } from './$types'
	
	// data returned from +page.server.ts
	export let data: PageData
  
  </script>
  
 
<div class="container h-full mx-auto flex justify-center items-center">
<div class="text-center">
	<h1 class="text-5xl font-bold mb-4">Tervetuloa Varaamoon!</h1>
	<p class="text-xl mb-4">Varaamon etusivu.</p>

	<!-- Loop through the data.feed array and display the equipment name -->
	{#each data.feed as equipment (equipment.id)}
		<p>{equipment.name}</p>
	{/each}

</div>
</div>
