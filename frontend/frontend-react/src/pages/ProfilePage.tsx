import React, { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';

const ProfilePage: React.FC = () => {
  const auth = useContext(AuthContext);
  const [firstName, setFirstName] = useState(auth?.user?.first_name || '');
  const [lastName, setLastName] = useState(auth?.user?.last_name || '');
  const [email, setEmail] = useState(auth?.user?.email || '');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  if (!auth || !auth.user) return <div>Loading user...</div>;

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    const updated = await auth.updateProfile({ first_name: firstName, last_name: lastName, email });
    if (updated) setMessage('Profile updated successfully');
    else setMessage('Failed to update profile');
    setSaving(false);
  };

  return (
    <div className="bg-neutral-100 min-h-full">
      <div className="kc-container py-8">
        <h1 className="text-2xl font-bold mb-4">Your Profile</h1>
        <form onSubmit={handleSave} className="bg-white p-6 rounded-lg shadow">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-neutral-700">First name</label>
              <input value={firstName} onChange={(e) => setFirstName(e.target.value)} className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md" />
            </div>
            <div>
              <label className="block text-sm font-medium text-neutral-700">Last name</label>
              <input value={lastName} onChange={(e) => setLastName(e.target.value)} className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md" />
            </div>
            <div>
              <label className="block text-sm font-medium text-neutral-700">Email</label>
              <input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md" />
            </div>
          </div>

          <div className="mt-6">
            <button type="submit" disabled={saving} className="bg-primary text-white px-4 py-2 rounded-md">
              {saving ? 'Saving...' : 'Save changes'}
            </button>
          </div>

          {message && <p className="mt-4 text-sm text-neutral-600">{message}</p>}
        </form>
      </div>
    </div>
  );
};

export default ProfilePage;