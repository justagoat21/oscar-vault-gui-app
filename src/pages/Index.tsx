
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import RegisterUser from '@/components/RegisterUser';
import Nominations from '@/components/Nominations';
import Statistics from '@/components/Statistics';
import DreamTeam from '@/components/DreamTeam';
import TopCompanies from '@/components/TopCompanies';

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-purple-800 text-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-yellow-200 mb-4">
            Academy Awards Vault
          </h1>
          <p className="text-purple-200 text-lg">
            Explore and Manage Oscar Nominations and Winners
          </p>
        </header>

        <Tabs defaultValue="register" className="w-full">
          <TabsList className="grid grid-cols-2 lg:grid-cols-6 gap-4 bg-purple-800/50 p-2 rounded-lg">
            <TabsTrigger value="register" className="text-white">Register</TabsTrigger>
            <TabsTrigger value="nominations" className="text-white">Nominations</TabsTrigger>
            <TabsTrigger value="statistics" className="text-white">Statistics</TabsTrigger>
            <TabsTrigger value="dreamteam" className="text-white">Dream Team</TabsTrigger>
            <TabsTrigger value="companies" className="text-white">Top Companies</TabsTrigger>
            <TabsTrigger value="movies" className="text-white">Foreign Films</TabsTrigger>
          </TabsList>

          <div className="mt-8">
            <TabsContent value="register">
              <RegisterUser />
            </TabsContent>
            <TabsContent value="nominations">
              <Nominations />
            </TabsContent>
            <TabsContent value="statistics">
              <Statistics />
            </TabsContent>
            <TabsContent value="dreamteam">
              <DreamTeam />
            </TabsContent>
            <TabsContent value="companies">
              <TopCompanies />
            </TabsContent>
            <TabsContent value="movies">
              <Card className="p-6 bg-white/10 backdrop-blur-lg">
                <h2 className="text-2xl font-semibold mb-4">Non-English Oscar Winners</h2>
                {/* This will be implemented in the next iteration */}
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </div>
  );
};

export default Index;
