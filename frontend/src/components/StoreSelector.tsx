import { useStore } from '@/contexts/StoreContext';

export function StoreSelector() {
  const { availableStores, selectedStore, selectStore, isLoading } = useStore();

  if (isLoading || availableStores.length === 0) {
    return null;
  }

  if (availableStores.length === 1) {
    return (
      <div className="text-sm text-gray-700 dark:text-gray-300">
        <span className="font-medium">{availableStores[0].store.name}</span>
      </div>
    );
  }

  return (
    <div className="relative">
      <select
        value={selectedStore?.store_id || ''}
        onChange={(e) => selectStore(parseInt(e.target.value))}
        className="block w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
      >
        {availableStores.map((storeAccess) => (
          <option key={storeAccess.store_id} value={storeAccess.store_id}>
            {storeAccess.store.name} ({storeAccess.scope})
          </option>
        ))}
      </select>
      <div className="mt-1 text-xs text-gray-500 dark:text-gray-400">
        Current Store
      </div>
    </div>
  );
}
