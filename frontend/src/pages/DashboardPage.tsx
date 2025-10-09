import { DashboardLayout } from '@/components/DashboardLayout';
import { useAuth } from '@/contexts/AuthContext';

export function DashboardPage() {
  const { user } = useAuth();

  return (
    <DashboardLayout>
      <div className="px-4 py-6 sm:px-0">
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome, {user?.first_name}!
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            You're successfully logged in to TSV-RSM.
          </p>
          
          <div className="mt-6 grid grid-cols-1 gap-4">
            <div className="border dark:border-gray-700 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Email
              </h3>
              <p className="mt-1 text-sm text-gray-900 dark:text-white">
                {user?.email}
              </p>
            </div>
            
            <div className="border dark:border-gray-700 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Status
              </h3>
              <p className="mt-1 text-sm text-gray-900 dark:text-white capitalize">
                {user?.status}
              </p>
            </div>
            
            <div className="border dark:border-gray-700 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Roles
              </h3>
              <div className="mt-1 flex flex-wrap gap-2">
                {user?.roles.map((role) => (
                  <span
                    key={role.id}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                  >
                    {role.name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
