const API_URL = 'https://amiapi.faneagain.ru';

export async function processMap(mapData) {
  // Transform frontend map data to match backend expectations
  const transformedData = {
    map: {
      w: mapData.width || 15,  // Default width if not provided
      h: mapData.height || 25,  // Default height if not provided
      desc: {
        name: mapData.name || 'Новая карта',
        desc: mapData.description || ''
      },
      tiles: mapData.tiles || {}  // Pass through the tiles data structure
    },
    chars: (mapData.characters || []).map(char => ({
      id: char.id,
      name: char.name,
      pos: char.position || [1, 1],  // Default position if not provided
      icon: char.icon,
      desc: char.description || '',  // Preserve character description
      stats: {
        hp: char.stats?.hp || 20,
        max: char.stats?.maxHp || 20,
        ac: char.stats?.ac || 10,
        str: char.stats?.strength || 10,
        dex: char.stats?.agility || 10,
        con: char.stats?.constitution || 10,
        int: char.stats?.intelligence || 10,
        wis: char.stats?.wisdom || 10,
        cha: char.stats?.charisma || 10
      },
      weapon: {
        name: char.weapon?.name || 'Меч',
        dmg: char.weapon?.damage || '1d8'
      },
      spells: (char.spells || []).map(spell => ({
        name: spell.name,
        effect: spell.damage || spell.healing || spell.effect
      }))
    })),
    turn: {
      order: (mapData.characters || []).map(char => char.name),
      current: mapData.characters?.[0]?.name || ''  // Set first character as current if exists
    }
  };

  try {
    const response = await fetch(`${API_URL}/process-map`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify(transformedData)
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    console.error('Error processing map:', error);
    throw error;
  }
} 