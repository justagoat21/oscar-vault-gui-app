
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";

const RegisterUser = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    birthDate: '',
    gender: '',
    country: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    toast({
      title: "Success",
      description: "User registered successfully!",
    });
  };

  return (
    <Card className="p-6 bg-white/10 backdrop-blur-lg">
      <h2 className="text-2xl font-semibold mb-6">Register New User</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm">Username</label>
            <Input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              className="bg-white/5"
              required
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm">Email</label>
            <Input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="bg-white/5"
              required
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm">Birth Date</label>
            <Input
              type="date"
              value={formData.birthDate}
              onChange={(e) => setFormData({...formData, birthDate: e.target.value})}
              className="bg-white/5"
              required
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm">Gender</label>
            <Input
              type="text"
              value={formData.gender}
              onChange={(e) => setFormData({...formData, gender: e.target.value})}
              className="bg-white/5"
              required
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm">Country</label>
            <Input
              type="text"
              value={formData.country}
              onChange={(e) => setFormData({...formData, country: e.target.value})}
              className="bg-white/5"
              required
            />
          </div>
        </div>
        <Button type="submit" className="w-full bg-yellow-500 hover:bg-yellow-600 text-black">
          Register User
        </Button>
      </form>
    </Card>
  );
};

export default RegisterUser;
