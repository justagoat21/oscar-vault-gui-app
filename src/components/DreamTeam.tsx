
import { Card } from "@/components/ui/card";

const DreamTeam = () => {
  return (
    <Card className="p-6 bg-white/10 backdrop-blur-lg">
      <h2 className="text-2xl font-semibold mb-6">Dream Team - Best Living Cast</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {['Director', 'Actor', 'Actress', 'Supporting Actor', 'Supporting Actress', 'Producer', 'Score Singer'].map((role) => (
          <Card key={role} className="p-4 bg-white/5">
            <h3 className="text-lg font-semibold mb-2">{role}</h3>
            <p className="text-purple-200">Loading...</p>
          </Card>
        ))}
      </div>
    </Card>
  );
};

export default DreamTeam;
