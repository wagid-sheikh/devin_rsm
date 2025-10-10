import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DashboardLayout } from '@/components/DashboardLayout';
import { CustomersService, type CustomerResponse, type CustomerContactResponse, type CustomerAddressResponse, type CustomerContactCreate, type CustomerContactUpdate, type CustomerAddressCreate, type CustomerAddressUpdate } from '@/lib/sdk';
import { ApiError } from '@/lib/sdk';

export function CustomerDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const customerId = parseInt(id || '0', 10);

  const [customer, setCustomer] = useState<CustomerResponse | null>(null);
  const [contacts, setContacts] = useState<CustomerContactResponse[]>([]);
  const [addresses, setAddresses] = useState<CustomerAddressResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'contacts' | 'addresses'>('info');
  
  const [showAddContact, setShowAddContact] = useState(false);
  const [showAddAddress, setShowAddAddress] = useState(false);

  const [contactForm, setContactForm] = useState<CustomerContactCreate>({
    contact_person: '',
    phone: '',
    email: undefined,
    is_primary: false,
  });

  const [addressForm, setAddressForm] = useState<CustomerAddressCreate>({
    type: '',
    address: '',
    is_pickup_default: false,
    is_delivery_default: false,
  });

  const loadCustomer = useCallback(async () => {
    try {
      setLoading(true);
      const data = await CustomersService.getCustomerApiV1CustomersCustomerIdGet(customerId);
      setCustomer(data);
      setContacts(data.contacts || []);
      setAddresses(data.addresses || []);
      setError(null);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load customer');
      }
    } finally {
      setLoading(false);
    }
  }, [customerId]);

  useEffect(() => {
    loadCustomer();
  }, [customerId, loadCustomer]);

  const handleAddContact = async () => {
    try {
      await CustomersService.createCustomerContactApiV1CustomersCustomerIdContactsPost(
        customerId,
        contactForm
      );
      setShowAddContact(false);
      setContactForm({
        contact_person: '',
        phone: '',
        email: undefined,
        is_primary: false,
      });
      await loadCustomer();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(`Error: ${err.message}`);
      } else {
        alert('Failed to create contact');
      }
    }
  };

  const handleUpdateContact = async (contactId: number, updates: CustomerContactUpdate) => {
    try {
      await CustomersService.updateCustomerContactApiV1CustomersCustomerIdContactsContactIdPatch(
        customerId,
        contactId,
        updates
      );
      await loadCustomer();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(`Error: ${err.message}`);
      } else {
        alert('Failed to update contact');
      }
    }
  };

  const handleDeleteContact = async (contactId: number) => {
    if (!confirm('Are you sure you want to delete this contact?')) return;
    
    try {
      await CustomersService.deleteCustomerContactApiV1CustomersCustomerIdContactsContactIdDelete(
        customerId,
        contactId
      );
      await loadCustomer();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(`Error: ${err.message}`);
      } else {
        alert('Failed to delete contact');
      }
    }
  };

  const handleAddAddress = async () => {
    try {
      await CustomersService.createCustomerAddressApiV1CustomersCustomerIdAddressesPost(
        customerId,
        addressForm
      );
      setShowAddAddress(false);
      setAddressForm({
        type: '',
        address: '',
        is_pickup_default: false,
        is_delivery_default: false,
      });
      await loadCustomer();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(`Error: ${err.message}`);
      } else {
        alert('Failed to create address');
      }
    }
  };

  const handleUpdateAddress = async (addressId: number, updates: CustomerAddressUpdate) => {
    try {
      await CustomersService.updateCustomerAddressApiV1CustomersCustomerIdAddressesAddressIdPatch(
        customerId,
        addressId,
        updates
      );
      await loadCustomer();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(`Error: ${err.message}`);
      } else {
        alert('Failed to update address');
      }
    }
  };

  const handleDeleteAddress = async (addressId: number) => {
    if (!confirm('Are you sure you want to delete this address?')) return;
    
    try {
      await CustomersService.deleteCustomerAddressApiV1CustomersCustomerIdAddressesAddressIdDelete(
        customerId,
        addressId
      );
      await loadCustomer();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(`Error: ${err.message}`);
      } else {
        alert('Failed to delete address');
      }
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">Loading customer...</p>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !customer) {
    return (
      <DashboardLayout>
        <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-4">
          <p className="text-sm text-red-800 dark:text-red-200">{error || 'Customer not found'}</p>
          <button
            onClick={() => navigate('/customers')}
            className="mt-2 text-sm text-red-600 hover:text-red-800 dark:text-red-400"
          >
            ← Back to customers
          </button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <button
              onClick={() => navigate('/customers')}
              className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 mb-2"
            >
              ← Back to customers
            </button>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{customer.name}</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {customer.code && `Code: ${customer.code} • `}
              {customer.phone_primary}
              {customer.email && ` • ${customer.email}`}
            </p>
          </div>
        </div>

        <div className="border-b border-gray-200 dark:border-gray-700">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('info')}
              className={`${
                activeTab === 'info'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Information
            </button>
            <button
              onClick={() => setActiveTab('contacts')}
              className={`${
                activeTab === 'contacts'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Contacts ({contacts.length})
            </button>
            <button
              onClick={() => setActiveTab('addresses')}
              className={`${
                activeTab === 'addresses'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Addresses ({addresses.length})
            </button>
          </nav>
        </div>

        {activeTab === 'info' && (
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
              <div>
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Customer Code</dt>
                <dd className="mt-1 text-sm text-gray-900 dark:text-white">{customer.code || '-'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Status</dt>
                <dd className="mt-1">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    customer.status === 'active'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  }`}>
                    {customer.status}
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Primary Phone</dt>
                <dd className="mt-1 text-sm text-gray-900 dark:text-white">{customer.phone_primary}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Email</dt>
                <dd className="mt-1 text-sm text-gray-900 dark:text-white">{customer.email || '-'}</dd>
              </div>
              <div className="sm:col-span-2">
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Notes</dt>
                <dd className="mt-1 text-sm text-gray-900 dark:text-white whitespace-pre-wrap">{customer.notes || '-'}</dd>
              </div>
            </dl>
          </div>
        )}

        {activeTab === 'contacts' && (
          <div className="space-y-4">
            <div className="flex justify-end">
              <button
                onClick={() => setShowAddContact(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                Add Contact
              </button>
            </div>

            <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Contact Person</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Phone</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Primary</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {contacts.map((contact) => (
                    <tr key={contact.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{contact.contact_person}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{contact.phone}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{contact.email || '-'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {contact.is_primary ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                            Primary
                          </span>
                        ) : (
                          <button
                            onClick={() => handleUpdateContact(contact.id, { is_primary: true })}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400"
                          >
                            Set as Primary
                          </button>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleDeleteContact(contact.id)}
                          className="text-red-600 hover:text-red-900 dark:text-red-400"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                  {contacts.length === 0 && (
                    <tr>
                      <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
                        No contacts found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'addresses' && (
          <div className="space-y-4">
            <div className="flex justify-end">
              <button
                onClick={() => setShowAddAddress(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                Add Address
              </button>
            </div>

            <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Address</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pickup Default</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Delivery Default</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {addresses.map((address) => (
                    <tr key={address.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{address.type}</td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">{address.address}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {address.is_pickup_default ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                            Default
                          </span>
                        ) : (
                          <button
                            onClick={() => handleUpdateAddress(address.id, { is_pickup_default: true })}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400"
                          >
                            Set Default
                          </button>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {address.is_delivery_default ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                            Default
                          </span>
                        ) : (
                          <button
                            onClick={() => handleUpdateAddress(address.id, { is_delivery_default: true })}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400"
                          >
                            Set Default
                          </button>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleDeleteAddress(address.id)}
                          className="text-red-600 hover:text-red-900 dark:text-red-400"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                  {addresses.length === 0 && (
                    <tr>
                      <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
                        No addresses found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {showAddContact && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Add Contact</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Contact Person</label>
                <input
                  type="text"
                  value={contactForm.contact_person}
                  onChange={(e) => setContactForm({ ...contactForm, contact_person: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Phone</label>
                <input
                  type="text"
                  value={contactForm.phone}
                  onChange={(e) => setContactForm({ ...contactForm, phone: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Email (Optional)</label>
                <input
                  type="email"
                  value={contactForm.email || ''}
                  onChange={(e) => setContactForm({ ...contactForm, email: e.target.value || undefined })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={contactForm.is_primary}
                  onChange={(e) => setContactForm({ ...contactForm, is_primary: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label className="ml-2 block text-sm text-gray-900 dark:text-white">Set as primary contact</label>
              </div>
            </div>
            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setShowAddContact(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600"
              >
                Cancel
              </button>
              <button
                onClick={handleAddContact}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                Add Contact
              </button>
            </div>
          </div>
        </div>
      )}

      {showAddAddress && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Add Address</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Type</label>
                <input
                  type="text"
                  value={addressForm.type}
                  onChange={(e) => setAddressForm({ ...addressForm, type: e.target.value })}
                  placeholder="e.g., Home, Office"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Address</label>
                <textarea
                  value={addressForm.address}
                  onChange={(e) => setAddressForm({ ...addressForm, address: e.target.value })}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={addressForm.is_pickup_default}
                  onChange={(e) => setAddressForm({ ...addressForm, is_pickup_default: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label className="ml-2 block text-sm text-gray-900 dark:text-white">Set as pickup default</label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={addressForm.is_delivery_default}
                  onChange={(e) => setAddressForm({ ...addressForm, is_delivery_default: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label className="ml-2 block text-sm text-gray-900 dark:text-white">Set as delivery default</label>
              </div>
            </div>
            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setShowAddAddress(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600"
              >
                Cancel
              </button>
              <button
                onClick={handleAddAddress}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                Add Address
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
