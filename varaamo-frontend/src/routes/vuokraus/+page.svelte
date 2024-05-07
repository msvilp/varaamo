<script lang="ts">
    import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
    import type { TableSource } from '@skeletonlabs/skeleton';
    import type { PageData } from './$types';

    export let data: PageData;

    const filteredData = data.feed.filter(equipment => equipment.visible === true);

    const sourceData = filteredData.map(equipment => ({
        name: equipment.name,
        count: equipment.count,
        rentable: equipment.rentable
    }));

    const tableSimple: TableSource = {
        head: ["Name", "Count", "Rentable"],
        body: tableMapperValues(sourceData, ["name", "count", "rentable"]),
        meta: tableMapperValues(sourceData, ["name", "count", "rentable"]),
    }
</script>

<h2>Vuokrattavat tuotteet</h2>

<div class="btn-group variant-filled">
	<button>Kajakit</button>
	<button>SUP-laudat</button>
</div>

<Table source={tableSimple} />
