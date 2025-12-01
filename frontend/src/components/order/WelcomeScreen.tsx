export default function WelcomeCustomer({
  startOrder,
}: {
  startOrder: (orderId:string)=> void;
}) {

  const handleStartOrder = async () => {
    try {
      const res = await new Promise<string>((resolve) => {
        setTimeout(() => {
          resolve("order1");
        }, 600);
      });
      startOrder(res);
    } catch (err) {
      console.error("API Error:", err);
    } 
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center p-8">
      <div className="text-center text-white">
        <h1>🍔 Fast Food Ordering System</h1>
        <p>Welcome to our ordering system!</p>
        <p className="text-2xl mb-12">Your favorite fast food, faster!</p>
        <button
          onClick={handleStartOrder}
          className="bg-white text-red-600 px-16 py-6 rounded-full text-3xl font-bold hover:bg-gray-100 transition shadow-2xl"
        >
          Tap to Start Order
        </button>
      </div>
    </div>
  );
}
