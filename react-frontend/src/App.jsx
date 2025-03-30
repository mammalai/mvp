// import { RouterProvider } from 'react-router-dom';

// // project import
// import router from 'routes';
// import ThemeCustomization from 'themes';

// import ScrollTop from 'components/ScrollTop';

// import { machineActor } from './store';

// // ==============================|| APP - THEME, ROUTER, LOCAL ||============================== //

// export default function App() {
//   machineActor.start();

//   return (
//     <ThemeCustomization>
//       <ScrollTop>
//         <RouterProvider router={router} />
//       </ScrollTop>
//     </ThemeCustomization>
//   );
// }

import React, { useState } from 'react';
import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';

// Renders errors or successfull transactions on the screen.
function Message({ content }) {
  return <p>{content}</p>;
}

function App() {
  const initialOptions = {
    'client-id': 'AdNSlo-AcCtKpbrI6W8kqda2hTQxIfAs-yQUspao_r1WIEgxkd7QywTFDVfWtUxLlWxk6Yyp-o4pp9Rs',
    'enable-funding': 'venmo',
    'disable-funding': '',
    'buyer-country': 'US',
    currency: 'USD',
    'data-page-type': 'product-details',
    components: 'buttons',
    'data-sdk-integration-source': 'developer-studio',
  };

  const [message, setMessage] = useState('');

  return (
    <div className="App">
      <PayPalScriptProvider options={initialOptions}>
        <PayPalButtons
          style={{
            shape: 'rect',
            layout: 'vertical',
            color: 'gold',
            label: 'paypal',
          }}
          createOrder={async () => {
            try {
              const response = await fetch('http://127.0.0.1:5000/api/orders', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                // use the "body" param to optionally pass additional order information
                // like product ids and quantities
                body: JSON.stringify({
                  cart: [
                    {
                      id: 'YOUR_PRODUCT_ID',
                      quantity: '1',
                    },
                  ],
                }),
              });

              const orderData = await response.json();

              console.log('Create Order', orderData);

              if (orderData.id) {
                return orderData.id;
              } else {
                const errorDetail = orderData?.details?.[0];
                const errorMessage = errorDetail
                  ? `${errorDetail.issue} ${errorDetail.description} (${orderData.debug_id})`
                  : JSON.stringify(orderData);

                throw new Error(errorMessage);
              }
            } catch (error) {
              console.error(error);
              setMessage(`Could not initiate PayPal Checkout...${error}`);
            }
          }}
          onApprove={async (data, actions) => {
            try {
              const response = await fetch(`http://127.0.0.1:5000/api/orders/${data.orderID}/capture`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
              });

              const orderData = await response.json();
              // Three cases to handle:
              //   (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
              //   (2) Other non-recoverable errors -> Show a failure message
              //   (3) Successful transaction -> Show confirmation or thank you message

              console.log('Capture Order', orderData);

              const errorDetail = orderData?.details?.[0];

              if (errorDetail?.issue === 'INSTRUMENT_DECLINED') {
                // (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
                // recoverable state, per https://developer.paypal.com/docs/checkout/standard/customize/handle-funding-failures/
                return actions.restart();
              } else if (errorDetail) {
                // (2) Other non-recoverable errors -> Show a failure message
                throw new Error(`${errorDetail.description} (${orderData.debug_id})`);
              } else {
                // (3) Successful transaction -> Show confirmation or thank you message
                // Or go to another URL:  actions.redirect('thank_you.html');
                const transaction = orderData.purchase_units[0].payments.captures[0];
                setMessage(`Transaction ${transaction.status}: ${transaction.id}. See console for all available details`);
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
              }
            } catch (error) {
              console.error(error);
              setMessage(`Sorry, your transaction could not be processed...${error}`);
            }
          }}
        />
      </PayPalScriptProvider>
      <Message content={message} />
    </div>
  );
}

export default App;
