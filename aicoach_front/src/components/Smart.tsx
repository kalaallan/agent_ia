import {} from "react";

interface SmartProps {
  resTrunk: string | null;
}

const Smart = ({ resTrunk }: SmartProps) => {
  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Smart Search</h2>
      {resTrunk && <p className="text-gray-700">{resTrunk}</p>}
    </div>
  );
}

export default Smart;