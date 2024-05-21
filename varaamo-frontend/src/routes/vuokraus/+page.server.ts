import prisma from '$lib/prisma';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    const equipmentItems = await prisma.equipment_equipmentitem.findMany({
        include: {
            equipment_equipmentclass: true
        }
    });

    const equipmentClass = await prisma.equipment_equipmentclass.findMany();

    return { equipmentItems: equipmentItems, equipmentClasses: equipmentClass };
}) satisfies PageServerLoad;