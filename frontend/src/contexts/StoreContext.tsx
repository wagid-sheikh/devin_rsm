import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { useAuth } from './AuthContext';

interface Store {
  id: number;
  name: string;
  company_id: number;
}

interface UserStoreAccess {
  id: number;
  store_id: number;
  scope: string;
  store: Store;
}

interface StoreContextType {
  availableStores: UserStoreAccess[];
  selectedStore: UserStoreAccess | null;
  isLoading: boolean;
  selectStore: (storeId: number) => void;
  clearStore: () => void;
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

const SELECTED_STORE_KEY = 'selected_store_id';

export function StoreProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [availableStores, setAvailableStores] = useState<UserStoreAccess[]>([]);
  const [selectedStore, setSelectedStore] = useState<UserStoreAccess | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user && user.store_accesses) {
      setAvailableStores(user.store_accesses);

      const savedStoreId = localStorage.getItem(SELECTED_STORE_KEY);
      if (savedStoreId) {
        const store = user.store_accesses.find(sa => sa.store_id === parseInt(savedStoreId));
        if (store) {
          setSelectedStore(store);
        } else if (user.store_accesses.length > 0) {
          setSelectedStore(user.store_accesses[0]);
          localStorage.setItem(SELECTED_STORE_KEY, user.store_accesses[0].store_id.toString());
        }
      } else if (user.store_accesses.length > 0) {
        setSelectedStore(user.store_accesses[0]);
        localStorage.setItem(SELECTED_STORE_KEY, user.store_accesses[0].store_id.toString());
      }

      setIsLoading(false);
    } else {
      setAvailableStores([]);
      setSelectedStore(null);
      setIsLoading(false);
    }
  }, [user]);

  const selectStore = (storeId: number) => {
    const store = availableStores.find(sa => sa.store_id === storeId);
    if (store) {
      setSelectedStore(store);
      localStorage.setItem(SELECTED_STORE_KEY, storeId.toString());
    }
  };

  const clearStore = () => {
    setSelectedStore(null);
    localStorage.removeItem(SELECTED_STORE_KEY);
  };

  return (
    <StoreContext.Provider
      value={{
        availableStores,
        selectedStore,
        isLoading,
        selectStore,
        clearStore,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useStore() {
  const context = useContext(StoreContext);
  if (context === undefined) {
    throw new Error('useStore must be used within a StoreProvider');
  }
  return context;
}
