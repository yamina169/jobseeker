//components/modal.jsx


export default function Modal({ children, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
      <div className="bg-white p-6 rounded shadow-lg min-w-[350px]">
        {children}
        <button
          className="mt-4 px-3 py-1 bg-gray-600 text-white rounded"
          onClick={onClose}
        >
          Fermer
        </button>
      </div>
    </div>
  );
}
