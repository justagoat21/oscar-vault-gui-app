
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";

const Nominations = () => {
  const { toast } = useToast();
  const [nominationForm, setNominationForm] = useState({
    email: '',
    movieName: '',
    releaseYear: '',
    category: '',
    staffFirstName: '',
    staffLastName: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "Success",
      description: "Nomination added successfully!",
    });
  };

  const [viewEmail, setViewEmail] = useState('');

  return (
    <Card className="p-6 bg-white/10 backdrop-blur-lg">
      <Tabs defaultValue="add">
        <TabsList className="mb-4">
          <TabsTrigger value="add">Add Nomination</TabsTrigger>
          <TabsTrigger value="view">View Nominations</TabsTrigger>
        </TabsList>
        
        <TabsContent value="add">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm">Email</label>
                <Input
                  type="email"
                  value={nominationForm.email}
                  onChange={(e) => setNominationForm({...nominationForm, email: e.target.value})}
                  className="bg-white/5"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm">Movie Name</label>
                <Input
                  type="text"
                  value={nominationForm.movieName}
                  onChange={(e) => setNominationForm({...nominationForm, movieName: e.target.value})}
                  className="bg-white/5"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm">Release Year</label>
                <Input
                  type="number"
                  value={nominationForm.releaseYear}
                  onChange={(e) => setNominationForm({...nominationForm, releaseYear: e.target.value})}
                  className="bg-white/5"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm">Category</label>
                <Input
                  type="text"
                  value={nominationForm.category}
                  onChange={(e) => setNominationForm({...nominationForm, category: e.target.value})}
                  className="bg-white/5"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm">Staff First Name</label>
                <Input
                  type="text"
                  value={nominationForm.staffFirstName}
                  onChange={(e) => setNominationForm({...nominationForm, staffFirstName: e.target.value})}
                  className="bg-white/5"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm">Staff Last Name</label>
                <Input
                  type="text"
                  value={nominationForm.staffLastName}
                  onChange={(e) => setNominationForm({...nominationForm, staffLastName: e.target.value})}
                  className="bg-white/5"
                  required
                />
              </div>
            </div>
            <Button type="submit" className="w-full bg-yellow-500 hover:bg-yellow-600 text-black">
              Add Nomination
            </Button>
          </form>
        </TabsContent>

        <TabsContent value="view">
          <div className="space-y-4">
            <div className="flex gap-4">
              <Input
                type="email"
                placeholder="Enter email to view nominations"
                value={viewEmail}
                onChange={(e) => setViewEmail(e.target.value)}
                className="bg-white/5"
              />
              <Button className="bg-yellow-500 hover:bg-yellow-600 text-black">
                View Nominations
              </Button>
            </div>
            <div className="mt-4">
              {/* Nominations will be displayed here */}
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
};

export default Nominations;
