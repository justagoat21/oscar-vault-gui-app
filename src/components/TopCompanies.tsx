
import { Card } from "@/components/ui/card";

const TopCompanies = () => {
  return (
    <Card className="p-6 bg-white/10 backdrop-blur-lg">
      <h2 className="text-2xl font-semibold mb-6">Top 5 Production Companies</h2>
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4">
          {[1, 2, 3, 4, 5].map((index) => (
            <Card key={index} className="p-4 bg-white/5">
              <div className="flex items-center justify-between">
                <span className="text-xl font-bold">{index}</span>
                <div className="text-right">
                  <p className="text-purple-200">Loading...</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </Card>
  );
};

export default TopCompanies;
