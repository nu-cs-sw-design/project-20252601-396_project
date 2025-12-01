import { useState } from "react";
import { ArrowLeft, ShoppingCart } from "lucide-react";
import WelcomeCustomer from "../components/order/WelcomeScreen";
import BrowseMenu from "../components/menu/BrowseMenu";
import CustomizeItem from "../components/menu/CustomizeItem";
import ReviewOrder from "../components/order/ReviewOrder";
import * as Types from "../types/index"

export default function CustomerUI() {
  const [orderId, setOrderId] = useState<string | null>(null);
  const [item, setItem] = useState<Types.MenuItem | null>(null);
  const [viewingOrder, setViewingOrder] = useState<boolean>(false);


  function handleReset(){
    setOrderId(null);
    setItem(null);
    setViewingOrder(false);

  }

  function handleGoBack() {

    if (viewingOrder){
        setViewingOrder(false);
        return;
    }

    if (item) {
      setItem(null);
      return;
    }

    if (orderId) {
      setOrderId(null);
      return;
    }
  }

  function OrderScreen() {

    if (orderId === null) {
      return <WelcomeCustomer startOrder={(orderId) => setOrderId(orderId)} />;
    }

    if (viewingOrder){
        return (<ReviewOrder orderId={orderId} handleReset={handleReset} />);
    }

    if (item == null) {
      return <BrowseMenu handleItemSelect={setItem} />;
    }

    return <CustomizeItem item={item} orderId={orderId} goBack={handleGoBack}/>

  }

  function ViewOrderButton() {
    if (orderId) {
      return (
        <div className="min-h-screen bg-gray-100">
          <div className="bg-red-600 text-white p-6 shadow-lg">
            <div className="flex justify-between items-center max-w-6xl mx-auto">
              <h1 className="text-4xl font-bold">Select Category</h1>
              <button
                onClick={() => setViewingOrder(true)}
                className="bg-white text-red-600 px-6 py-3 rounded-full font-bold flex items-center gap-2 hover:bg-gray-100"
              >
                <ShoppingCart size={24} />
                View Order
              </button>
            </div>
          </div>
        </div>
      );
    }else{
      return <div></div>
    }
  }

  function GoBackButton() {
    return (
      <div className="bg-red-600 text-white p-6 shadow-lg">
        <div className="flex items-center gap-4 max-w-6xl mx-auto">
          <button
            onClick={handleGoBack}
            className="hover:bg-red-700 p-2 rounded"
          >
            <ArrowLeft size={32} />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <GoBackButton />
      <ViewOrderButton />
      <div>
        <OrderScreen />
      </div>
    </div>
  );
}
