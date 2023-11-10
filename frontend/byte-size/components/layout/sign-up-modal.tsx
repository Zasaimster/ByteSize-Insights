import Modal from "@/components/shared/modal";
import { signIn } from "next-auth/react";
import {
    useState,
    Dispatch,
    SetStateAction,
    useCallback,
    useMemo,
} from "react";

const SignUpModal = ({
    showSignUpModal,
    setShowSignUpModal,
}: {
    showSignUpModal: boolean;
    setShowSignUpModal: Dispatch<SetStateAction<boolean>>;
}) => {
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        password: ""
    })

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target
        setFormData({
            ...formData,
            [name]: value
        })
    }
    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault()
        console.log(formData)
    }
    return (
        <Modal showModal={showSignUpModal} setShowModal={setShowSignUpModal}>
            <div className="w-full overflow-hidden shadow-xl md:max-w-md md:rounded-2xl md:border md:border-gray-200">
                <div className="flex flex-col items-center justify-center space-y-3 border-b border-gray-200 bg-white px-4 py-6 pt-8 text-center md:px-16">
                    <h3 className="font-display text-2xl font-bold">Sign Up</h3>
                    <p className="text-sm text-gray-500">
                        Sign up to receive email alerts and follow your favorite repositories.
                    </p>
                </div>

                <div className="flex flex-col space-y-4 bg-gray-50 px-4 py-8 md:px-16">
                    <div className="flex min-h-full px-6 lg:px-8">
                        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                            <form className="space-y-6" onSubmit={handleSubmit}>
                                <div className="flex space-x-4">
                                    <div className="sm:col-span-3">
                                        <label htmlFor="firstName" className="block text-sm font-medium leading-6 text-gray-900">First name</label>
                                        <div className="mt-2">
                                            <input type="text" name="firstName" id="firstName" autoComplete="family-name" onChange={handleInputChange} className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                                        </div>
                                    </div>
                                    <div className="sm:col-span-3">
                                        <label htmlFor="lastName" className="block text-sm font-medium leading-6 text-gray-900">Last name</label>
                                        <div className="mt-2">
                                            <input type="text" name="lastName" id="lastName" autoComplete="family-name" onChange={handleInputChange} className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <label
                                        htmlFor="email"
                                        className="block text-sm font-medium leading-6 text-gray-900"
                                    >
                                        Email address
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            id="email"
                                            name="email"
                                            type="email"
                                            autoComplete="email"
                                            onChange={handleInputChange}
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex items-center justify-between">
                                        <label
                                            htmlFor="password"
                                            className="block text-sm font-medium leading-6 text-gray-900"
                                        >
                                            Password
                                        </label>
                                    </div>
                                    <div className="mt-2">
                                        <input
                                            id="password"
                                            name="password"
                                            type="password"
                                            autoComplete="current-password"
                                            onChange={handleInputChange}
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <button
                                        type="submit"
                                        className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    >
                                        Sign Up
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>

                </div>
            </div>
        </Modal>
    );
};

export function useSignUpModal() {
    const [showSignUpModal, setShowSignUpModal] = useState(false);

    const SignUpModalCallback = useCallback(() => {
        return (
            <SignUpModal
                showSignUpModal={showSignUpModal}
                setShowSignUpModal={setShowSignUpModal}
            />
        );
    }, [showSignUpModal, setShowSignUpModal]);

    return useMemo(
        () => ({ setShowSignUpModal, SignUpModal: SignUpModalCallback }),
        [setShowSignUpModal, SignUpModalCallback],
    );
}