<script lang="ts">
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
	import type { TableSource } from '@skeletonlabs/skeleton';
	import type { PageData } from './$types';

	export let data: PageData;

	var selectedClass: string = '';

	function setTableSource():TableSource {
		let filteredEquipmentItems = data.equipmentItems.filter(
			(equipment) => equipment.visible === true
		);

		if (selectedClass !== '') {
			filteredEquipmentItems = filteredEquipmentItems.filter(
				(equipment) => equipment.equipment_equipmentclass.slug === selectedClass
			);
		}

		const equipmentItemTableData = filteredEquipmentItems.map((equipment) => ({
			name: equipment.name,
			count: equipment.count,
			rentable: equipment.rentable
		}));

		return {
			head: ['Name', 'Count', 'Rentable'],
			body: tableMapperValues(equipmentItemTableData, ['name', 'count', 'rentable']),
			meta: tableMapperValues(equipmentItemTableData, ['name', 'count', 'rentable'])
		};
	}
    let tableSimple = undefined;

    $: tableSimple = selectedClass != null ? setTableSource() : undefined;
</script>

<h2>Vuokrattavat tuotteet</h2>

<div class="btn-group variant-filled">
	{#each data.equipmentClasses as category (category.id)}
		<button class="btn" on:click={() => (selectedClass = category.slug)}>{category.name}</button>
	{/each}
    <button class="btn" on:click={() => (selectedClass = "")}>Kaikki</button>
</div>

<Table source={tableSimple} />
