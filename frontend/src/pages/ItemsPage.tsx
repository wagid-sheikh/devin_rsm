import React, { useCallback, useEffect, useState } from "react";
import { DashboardLayout } from "@/components/DashboardLayout";
import { ItemsService, type ItemCreate, type ItemResponse, type ItemUpdate, ApiError } from "@/lib/sdk";

function ItemsPage() {
  const [items, setItems] = useState<ItemResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [typeFilter, setTypeFilter] = useState<string>("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState<ItemResponse | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ItemsService.listItemsApiV1ItemsGet(
        search || undefined,
        statusFilter || undefined,
        typeFilter || undefined
      );
      setItems(data);
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to load items. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }, [search, statusFilter, typeFilter]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleCreate = async (data: ItemCreate | ItemUpdate) => {
    try {
      await ItemsService.createItemApiV1ItemsPost(data as ItemCreate);
      setShowCreateModal(false);
      await loadItems();
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        alert(err.message);
      } else {
        alert("Failed to create item. Please try again.");
      }
    }
  };

  const handleUpdate = async (data: ItemCreate | ItemUpdate) => {
    if (!selectedItem) return;
    try {
      await ItemsService.updateItemApiV1ItemsItemIdPatch(selectedItem.id, data as ItemUpdate);
      setShowEditModal(false);
      setSelectedItem(null);
      await loadItems();
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        alert(err.message);
      } else {
        alert("Failed to update item. Please try again.");
      }
    }
  };

  const handleToggleStatus = async (item: ItemResponse) => {
    const newStatus = item.status === "active" ? "inactive" : "active";
    try {
      await ItemsService.updateItemApiV1ItemsItemIdPatch(item.id, { status: newStatus });
      await loadItems();
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        alert(err.message);
      } else {
        alert("Failed to toggle status. Please try again.");
      }
    }
  };

  if (loading && items.length === 0) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-600 dark:text-gray-400">Loading items...</div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Items
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your items and services
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-800 dark:text-red-200">{error}</p>
          </div>
        )}

        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            placeholder="Search by SKU or name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Types</option>
            <option value="service">Service</option>
            <option value="product">Product</option>
          </select>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            Add Item
          </button>
        </div>

        {items.length === 0 ? (
          <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <p className="text-gray-600 dark:text-gray-400 mb-4">No items found</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              Create Your First Item
            </button>
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    SKU
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    UOM
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Tax Rate
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      {item.sku}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {item.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      <span className="capitalize">{item.type}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      <span className="uppercase">{item.uom}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      {item.tax_rate}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          item.status === "active"
                            ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                            : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400"
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                      <button
                        onClick={() => {
                          setSelectedItem(item);
                          setShowEditModal(true);
                        }}
                        className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleToggleStatus(item)}
                        className={`${
                          item.status === "active"
                            ? "text-orange-600 hover:text-orange-900 dark:text-orange-400 dark:hover:text-orange-300"
                            : "text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                        }`}
                      >
                        {item.status === "active" ? "Deactivate" : "Activate"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {showCreateModal && (
          <ItemFormModal
            title="Create Item"
            onClose={() => setShowCreateModal(false)}
            onSubmit={handleCreate}
          />
        )}

        {showEditModal && selectedItem && (
          <ItemFormModal
            title="Edit Item"
            initialData={selectedItem}
            onClose={() => {
              setShowEditModal(false);
              setSelectedItem(null);
            }}
            onSubmit={handleUpdate}
          />
        )}
      </div>
    </DashboardLayout>
  );
}

export default ItemsPage;

interface ItemFormModalProps {
  title: string;
  initialData?: ItemResponse;
  onClose: () => void;
  onSubmit: (data: ItemCreate | ItemUpdate) => Promise<void>;
}

function ItemFormModal({ title, initialData, onClose, onSubmit }: ItemFormModalProps) {
  const [formData, setFormData] = useState({
    sku: initialData?.sku || "",
    name: initialData?.name || "",
    type: initialData?.type || "service",
    hsn_sac: initialData?.hsn_sac || "",
    uom: initialData?.uom || "piece",
    tax_rate: initialData?.tax_rate?.toString() || "0",
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit({
        ...formData,
        hsn_sac: formData.hsn_sac || undefined,
        tax_rate: parseFloat(formData.tax_rate),
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          {title}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              SKU *
            </label>
            <input
              type="text"
              required
              value={formData.sku}
              onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Name *
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Type *
            </label>
            <select
              required
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="service">Service</option>
              <option value="product">Product</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              HSN/SAC
            </label>
            <input
              type="text"
              value={formData.hsn_sac}
              onChange={(e) => setFormData({ ...formData, hsn_sac: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Unit of Measurement *
            </label>
            <select
              required
              value={formData.uom}
              onChange={(e) => setFormData({ ...formData, uom: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="piece">Piece</option>
              <option value="kg">Kg</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Tax Rate (%) *
            </label>
            <input
              type="number"
              required
              min="0"
              max="100"
              step="0.01"
              value={formData.tax_rate}
              onChange={(e) => setFormData({ ...formData, tax_rate: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium disabled:opacity-50"
            >
              {submitting ? "Saving..." : initialData ? "Update" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
