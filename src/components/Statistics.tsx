
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const Statistics = () => {
  const [nominatedPerson, setNominatedPerson] = useState({
    firstName: '',
    lastName: ''
  });

  return (
    <Card className="p-6 bg-white/10 backdrop-blur-lg">
      <h2 className="text-2xl font-semibold mb-6">Statistics</h2>
      
      <Tabs defaultValue="movies">
        <TabsList className="mb-4">
          <TabsTrigger value="movies">Top Movies</TabsTrigger>
          <TabsTrigger value="nominated">Nominated Person</TabsTrigger>
          <TabsTrigger value="countries">Top Countries</TabsTrigger>
        </TabsList>

        <TabsContent value="movies">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold">Search by Year</h3>
            <div className="flex gap-4">
              <Input
                type="number"
                placeholder="Enter year"
                className="bg-white/5"
              />
              <Button className="bg-yellow-500 hover:bg-yellow-600 text-black">
                Search
              </Button>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="nominated">
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                type="text"
                placeholder="First Name"
                value={nominatedPerson.firstName}
                onChange={(e) => setNominatedPerson({...nominatedPerson, firstName: e.target.value})}
                className="bg-white/5"
              />
              <Input
                type="text"
                placeholder="Last Name"
                value={nominatedPerson.lastName}
                onChange={(e) => setNominatedPerson({...nominatedPerson, lastName: e.target.value})}
                className="bg-white/5"
              />
            </div>
            <Button className="w-full bg-yellow-500 hover:bg-yellow-600 text-black">
              View Nominations & Wins
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="countries">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold">Top Birth Countries for Best Actor Winners</h3>
            {/* Results will be displayed here */}
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
};

export default Statistics;
